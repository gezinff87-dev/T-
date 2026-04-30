import requests
import json
import time
import sys
import random
import string
import os
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Mostra banner simples do programa"""
    clear_screen()
    print(f"""{Fore.CYAN}
    ╔══════════════════════════════════════╗
    ║        NITRO CHECKER v1.0           ║
    ╚══════════════════════════════════════╝
    {Style.RESET_ALL}""")

def generate_nitro_link():
    """Gera um link de Nitro válido no formato correto"""
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(22))
    link = f"https://discord.com/billing/promotions/{codigo}"
    return link

def generate_links():
    """Função para gerar múltiplos links Nitro"""
    show_banner()
    print(f"{Fore.YELLOW}=== GERAR LINKS NITRO ==={Style.RESET_ALL}\n")
    
    try:
        quantidade = int(input("Quantos links você quer gerar? "))
        if quantidade <= 0:
            print(f"{Fore.RED}Digite um número positivo!{Style.RESET_ALL}")
            input("\nPressione Enter para continuar...")
            return
    except ValueError:
        print(f"{Fore.RED}Digite um número válido!{Style.RESET_ALL}")
        input("\nPressione Enter para continuar...")
        return
    
    nome_arquivo = input("Nome do arquivo para salvar (padrão: nitro_links.txt): ").strip()
    if not nome_arquivo:
        nome_arquivo = "nitro_links.txt"
    
    print(f"\n{Fore.CYAN}Gerando {quantidade} links...{Style.RESET_ALL}\n")
    
    links = []
    for i in range(quantidade):
        link = generate_nitro_link()
        links.append(link)
        print(f"[{i+1}/{quantidade}] {link}")
        time.sleep(0.05)
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
    
    print(f"\n{Fore.GREEN}✓ {quantidade} links salvos em '{nome_arquivo}'{Style.RESET_ALL}")
    input("\nPressione Enter para voltar ao menu...")

def check_single_link():
    """Verifica um único link Nitro"""
    show_banner()
    print(f"{Fore.YELLOW}=== VERIFICAR UM LINK ==={Style.RESET_ALL}\n")
    
    link = input("Cole o link Nitro: ").strip()
    
    if not link:
        print(f"{Fore.RED}Nenhum link fornecido!{Style.RESET_ALL}")
        input("\nPressione Enter para continuar...")
        return
    
    # Extrair o código do link se for URL completa
    if "discord.com/billing/promotions/" in link or "discord.gift/" in link:
        codigo = link.split('/')[-1]
    else:
        codigo = link
    
    print(f"\n{Fore.CYAN}Verificando: {codigo}{Style.RESET_ALL}")
    
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{codigo}?with_application=false&with_subscription_plan=true"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"\n{Fore.GREEN}✓ VÁLIDO!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Código: {codigo}{Style.RESET_ALL}")
            
            if 'subscription_plan' in dados:
                plano = dados['subscription_plan']['name']
                print(f"{Fore.GREEN}Plano: {plano}{Style.RESET_ALL}")
            
            # Salvar código válido
            with open('validos.txt', 'a', encoding='utf-8') as f:
                f.write(f"{link}\n")
            print(f"{Fore.GREEN}Salvo em 'validos.txt'{Style.RESET_ALL}")
            
        elif response.status_code == 429:
            print(f"{Fore.YELLOW}⚠ Rate limit - Aguarde um momento{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ INVÁLIDO (Status: {response.status_code}){Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Erro na verificação: {str(e)}{Style.RESET_ALL}")
    
    input("\nPressione Enter para voltar ao menu...")

def check_links_from_file():
    """Verifica links Nitro a partir de um arquivo"""
    show_banner()
    print(f"{Fore.YELLOW}=== VERIFICAR LINKS DE ARQUIVO ==={Style.RESET_ALL}\n")
    
    # Mostrar arquivos .txt disponíveis
    print(f"{Fore.CYAN}Arquivos .txt disponíveis:{Style.RESET_ALL}")
    arquivos_txt = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    if arquivos_txt:
        for i, arquivo in enumerate(arquivos_txt, 1):
            print(f"  [{i}] {arquivo}")
        print(f"  [0] Digitar nome manualmente")
        
        try:
            escolha = int(input("\nEscolha o número do arquivo: "))
            if escolha == 0:
                arquivo_escolhido = input("Digite o nome do arquivo: ").strip()
            elif 1 <= escolha <= len(arquivos_txt):
                arquivo_escolhido = arquivos_txt[escolha - 1]
            else:
                print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                input("\nPressione Enter para continuar...")
                return
        except ValueError:
            print(f"{Fore.RED}Digite um número válido!{Style.RESET_ALL}")
            input("\nPressione Enter para continuar...")
            return
    else:
        print(f"{Fore.YELLOW}Nenhum arquivo .txt encontrado{Style.RESET_ALL}")
        arquivo_escolhido = input("\nDigite o nome do arquivo: ").strip()
    
    # Verificar se arquivo existe
    if not os.path.exists(arquivo_escolhido):
        print(f"{Fore.RED}Arquivo '{arquivo_escolhido}' não encontrado!{Style.RESET_ALL}")
        input("\nPressione Enter para continuar...")
        return
    
    # Ler links do arquivo
    try:
        with open(arquivo_escolhido, 'r', encoding='utf-8') as f:
            links = [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"{Fore.RED}Erro ao ler arquivo: {str(e)}{Style.RESET_ALL}")
        input("\nPressione Enter para continuar...")
        return
    
    if not links:
        print(f"{Fore.RED}Arquivo vazio!{Style.RESET_ALL}")
        input("\nPressione Enter para continuar...")
        return
    
    print(f"\n{Fore.CYAN}{len(links)} links encontrados{Style.RESET_ALL}")
    
    # Configurar webhook (opcional)
    usar_webhook = input("\nUsar webhook do Discord? (s/n): ").strip().lower()
    webhook_url = ""
    if usar_webhook == 's':
        webhook_url = input("URL do webhook: ").strip()
    
    input(f"\n{Fore.YELLOW}Pressione Enter para iniciar a verificação...{Style.RESET_ALL}")
    
    validos = 0
    invalidos = 0
    
    print(f"\n{Fore.CYAN}Iniciando verificação...{Style.RESET_ALL}\n")
    
    with open('validos.txt', 'a', encoding='utf-8') as arquivo_validos:
        for i, link in enumerate(links, 1):
            # Extrair código
            if "discord.com/billing/promotions/" in link or "discord.gift/" in link:
                codigo = link.split('/')[-1]
            else:
                codigo = link
            
            url = f"https://discord.com/api/v9/entitlements/gift-codes/{codigo}?with_application=false&with_subscription_plan=true"
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"[{i}/{len(links)}] {Fore.GREEN}✓ VÁLIDO{Style.RESET_ALL} - {codigo}")
                    arquivo_validos.write(f"{link}\n")
                    validos += 1
                    
                    # Enviar webhook se configurado
                    if webhook_url:
                        try:
                            requests.post(webhook_url, json={
                                "content": f"🎉 **Nitro Válido!**\n{link}"
                            })
                        except:
                            pass
                            
                elif response.status_code == 429:
                    print(f"[{i}/{len(links)}] {Fore.YELLOW}⚠ Rate Limit{Style.RESET_ALL} - Aguardando...")
                    time.sleep(5)
                else:
                    print(f"[{i}/{len(links)}] {Fore.RED}✗ INVÁLIDO{Style.RESET_ALL} - {codigo}")
                    invalidos += 1
                    
                time.sleep(0.5)  # Delay para evitar rate limit
                
            except Exception as e:
                print(f"[{i}/{len(links)}] {Fore.RED}✗ ERRO{Style.RESET_ALL} - {str(e)[:50]}")
                invalidos += 1
    
    # Resultados
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Válidos: {validos}{Style.RESET_ALL}")
    print(f"{Fore.RED}✗ Inválidos: {invalidos}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total: {len(links)}{Style.RESET_ALL}")
    
    if validos > 0:
        print(f"\n{Fore.GREEN}Códigos válidos salvos em 'validos.txt'{Style.RESET_ALL}")
    
    input("\nPressione Enter para voltar ao menu...")

def main_menu():
    """Menu principal do programa"""
    while True:
        show_banner()
        print(f"{Fore.WHITE}[1]{Style.RESET_ALL} {Fore.GREEN}Gerar links Nitro{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2]{Style.RESET_ALL} {Fore.BLUE}Verificar links{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[3]{Style.RESET_ALL} {Fore.RED}Sair{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*40}{Style.RESET_ALL}")
        
        opcao = input(f"{Fore.WHITE}Escolha: {Style.RESET_ALL}").strip()
        
        if opcao == '1':
            generate_links()
        elif opcao == '2':
            verify_menu()
        elif opcao == '3':
            print(f"\n{Fore.YELLOW}Saindo...{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
            time.sleep(1)

def verify_menu():
    """Submenu de verificação"""
    while True:
        show_banner()
        print(f"{Fore.YELLOW}=== VERIFICAR LINKS ==={Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}[1]{Style.RESET_ALL} Verificar um link")
        print(f"{Fore.WHITE}[2]{Style.RESET_ALL} Verificar links de arquivo")
        print(f"{Fore.WHITE}[3]{Style.RESET_ALL} Voltar ao menu principal")
        print(f"{Fore.CYAN}{'─'*40}{Style.RESET_ALL}")
        
        opcao = input(f"{Fore.WHITE}Escolha: {Style.RESET_ALL}").strip()
        
        if opcao == '1':
            check_single_link()
        elif opcao == '2':
            check_links_from_file()
        elif opcao == '3':
            break
        else:
            print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programa encerrado.{Style.RESET_ALL}")
        sys.exit(0)
