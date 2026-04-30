import requests
import json
import time
import sys
import random
import string
import os
from colorama import init, Fore, Style

init()  # Initialize colorama

def animate_cover():
    sys.stdout.write("""
                                                                                                                            .sSSSSs.    
.sSSSSs.    .sSSSSs.    .sSSSs.  SSSSS      .sSSSs.  SSSSS SSSSS .sSSSSSSSSSSSSSs. .sSSSSSSSs. .sSSSSs.         .sSSS s.    `SSSS SSSs. 
S SSSSSSSs. S SSSSSSSs. S SSS SS SSSSS      S SSS SS SSSSS S SSS SSSSS S SSS SSSSS S SSS SSSSS S SSSSSSSs.      S SSS SSSs.       SSSSS 
S  SS SSSS' S  SS SSSS' S  SS  `sSSSSS      S  SS  `sSSSSS S  SS SSSSS S  SS SSSSS S  SS SSSS' S  SS SSSSS      S  SS SSSSS .sSSSsSSSS' 
S..SS       S..SS       S..SS    SSSSS      S..SS    SSSSS S..SS `:S:' S..SS `:S:' S..SSsSSSa. S..SS SSSSS      S..SS SSSSS S..SS       
S:::S`sSSs. S:::SSSS    S:::S    SSSSS      S:::S    SSSSS S:::S       S:::S       S:::S SSSSS S:::S SSSSS       S::S SSSS  S:::S SSSs. 
S;;;S SSSSS S;;;S       S;;;S    SSSSS      S;;;S    SSSSS S;;;S       S;;;S       S;;;S SSSSS S;;;S SSSSS        S;S SSS   S;;;S SSSSS 
S%%%S SSSSS S%%%S SSSSS S%%%S    SSSSS      S%%%S    SSSSS S%%%S       S%%%S       S%%%S SSSSS S%%%S SSSSS         SS SS    S%%%S SSSSS 
SSSSSsSSSSS SSSSSsSS;:' SSSSS    SSSSS      SSSSS    SSSSS SSSSS       SSSSS       SSSSS SSSSS SSSSSsSSSSS          SsS     SSSSSsSSSSS 
                                                                                                                                        
                                                                         """)
    sys.stdout.write("\n")
    sys.stdout.write("NitroChecker")
    sys.stdout.write("\n")
    sys.stdout.write("Loading")
    start_time = time.time()
    stop_time = start_time + random.uniform(5, 10)

    while time.time() < stop_time:
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\b \b" * 3)
        sys.stdout.flush()
        time.sleep(0.5)

    sys.stdout.write("\r")
    sys.stdout.write(" " * 13)
    sys.stdout.write("\r")
    sys.stdout.flush()
    time.sleep(1.5)  # 1.5 seconds pause

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_nitro_link():
    """Gera um link Nitro no formato correto"""
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(22))
    return f"https://discord.com/billing/promotions/{codigo}"

def generate_links():
    """Opção 1: Gerar links Nitro"""
    clear_screen()
    print(f"{Fore.WHITE}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║        GERAR LINKS NITRO             ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╚══════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    try:
        quantidade = int(input("Quantos links você quer gerar? "))
        if quantidade <= 0:
            print(f"{Fore.RED}Número deve ser positivo!{Style.RESET_ALL}")
            input("Pressione Enter para voltar...")
            return
    except ValueError:
        print(f"{Fore.RED}Digite um número válido!{Style.RESET_ALL}")
        input("Pressione Enter para voltar...")
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
    input("Pressione Enter para voltar ao menu...")

def send_webhook(url, content):
    """Envia resultado para webhook (opcional)"""
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(url, data=json.dumps(data), headers=headers)
    except:
        pass

def check_single_link():
    """Verificar um único link"""
    clear_screen()
    print(f"{Fore.WHITE}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║      VERIFICAR UM LINK               ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╚══════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    link = input("Cole o link ou código Nitro: ").strip()
    if not link:
        print(f"{Fore.RED}Nenhum dado informado!{Style.RESET_ALL}")
        input("Pressione Enter para voltar...")
        return
    
    # Extrai o código, caso seja uma URL completa
    if "/" in link:
        codigo = link.split('/')[-1]
    else:
        codigo = link
    
    print(f"\n{Fore.CYAN}Verificando: {codigo}{Style.RESET_ALL}")
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{codigo}?with_application=false&with_subscription_plan=true"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"\n{Fore.GREEN}✓ VÁLIDO!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Código: {codigo}{Style.RESET_ALL}")
            # Salva no arquivo de válidos
            with open('validos.txt', 'a', encoding='utf-8') as f:
                f.write(f"{link}\n")
            print(f"{Fore.GREEN}Salvo em 'validos.txt'{Style.RESET_ALL}")
        elif response.status_code == 429:
            print(f"{Fore.YELLOW}⚠ Rate limit - tente novamente mais tarde{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ INVÁLIDO (Status: {response.status_code}){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Erro: {str(e)}{Style.RESET_ALL}")
    
    input("\nPressione Enter para voltar...")

def check_links_from_file():
    """Verificar links a partir de um arquivo"""
    clear_screen()
    print(f"{Fore.WHITE}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║    VERIFICAR LINKS DE ARQUIVO        ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╚══════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Arquivos .txt disponíveis:{Style.RESET_ALL}")
    arquivos = [f for f in os.listdir('.') if f.endswith('.txt')]
    if arquivos:
        for i, arq in enumerate(arquivos, 1):
            print(f"  [{i}] {arq}")
        print(f"  [0] Digitar nome manualmente")
        
        try:
            opcao = int(input("\nEscolha: "))
            if opcao == 0:
                nome_arquivo = input("Nome do arquivo: ").strip()
            elif 1 <= opcao <= len(arquivos):
                nome_arquivo = arquivos[opcao-1]
            else:
                print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                input("Pressione Enter para voltar...")
                return
        except ValueError:
            print(f"{Fore.RED}Digite um número!{Style.RESET_ALL}")
            input("Pressione Enter para voltar...")
            return
    else:
        print(f"{Fore.YELLOW}Nenhum arquivo .txt encontrado.{Style.RESET_ALL}")
        nome_arquivo = input("Digite o nome do arquivo: ").strip()
    
    if not os.path.exists(nome_arquivo):
        print(f"{Fore.RED}Arquivo '{nome_arquivo}' não existe!{Style.RESET_ALL}")
        input("Pressione Enter para voltar...")
        return
    
    # Lê os links
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            links = [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"{Fore.RED}Erro ao ler o arquivo: {e}{Style.RESET_ALL}")
        input("Pressione Enter para voltar...")
        return
    
    if not links:
        print(f"{Fore.RED}Arquivo vazio!{Style.RESET_ALL}")
        input("Pressione Enter para voltar...")
        return
    
    print(f"\n{Fore.CYAN}{len(links)} links carregados.{Style.RESET_ALL}")
    
    # Webhook opcional
    usar_webhook = input("Enviar válidos para webhook do Discord? (s/n): ").strip().lower()
    webhook_url = ""
    if usar_webhook == 's':
        webhook_url = input("URL do webhook: ").strip()
    
    input(f"\n{Fore.YELLOW}Pressione Enter para começar a verificação...{Style.RESET_ALL}")
    
    validos = 0
    invalidos = 0
    
    print()
    with open('validos.txt', 'a', encoding='utf-8') as val_file:
        for i, link in enumerate(links, 1):
            # Extrai código
            if "/" in link:
                code = link.split('/')[-1]
            else:
                code = link
            
            url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    print(f"[{i}/{len(links)}] {Fore.GREEN}✓ VÁLIDO{Style.RESET_ALL} - {code}")
                    val_file.write(f"{link}\n")
                    validos += 1
                    if webhook_url:
                        send_webhook(webhook_url, f"🎉 Nitro válido: {link}")
                elif resp.status_code == 429:
                    print(f"[{i}/{len(links)}] {Fore.YELLOW}⚠ RATE LIMIT{Style.RESET_ALL}")
                    time.sleep(5)
                else:
                    print(f"[{i}/{len(links)}] {Fore.RED}✗ INVÁLIDO{Style.RESET_ALL} - {code}")
                    invalidos += 1
                    
                time.sleep(0.1)  # evita bloqueio
                
            except Exception as e:
                print(f"[{i}/{len(links)}] {Fore.RED}✗ ERRO{Style.RESET_ALL} - {str(e)[:50]}")
                invalidos += 1
    
    print(f"\n{Fore.WHITE}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║   RESULTADO                          ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╠══════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║ {Fore.GREEN}Válidos: {validos}{Style.RESET_ALL}                           {Fore.WHITE}║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║ {Fore.RED}Inválidos: {invalidos}{Style.RESET_ALL}                         {Fore.WHITE}║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    if validos > 0:
        print(f"\n{Fore.GREEN}Links válidos salvos em 'validos.txt'{Style.RESET_ALL}")
    input("\nPressione Enter para voltar ao menu...")

def show_menu():
    """Exibe o menu principal contornado em branco"""
    clear_screen()
    print(f"{Fore.WHITE}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║           MENU PRINCIPAL             ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╠══════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║  1. Gerar links Nitro                ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║  2. Verificar links                  ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}║  3. Sair                             ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    return input(f"\n{Fore.WHITE}Escolha uma opção: {Style.RESET_ALL}").strip()

def verify_submenu():
    """Submenu de verificação"""
    while True:
        clear_screen()
        print(f"{Fore.WHITE}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║        VERIFICAR LINKS               ║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}╠══════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║  1. Verificar um link                ║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║  2. Verificar links de arquivo       ║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║  3. Voltar ao menu principal         ║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}╚══════════════════════════════════════╝{Style.RESET_ALL}")
        op = input(f"\n{Fore.WHITE}Escolha: {Style.RESET_ALL}").strip()
        
        if op == '1':
            check_single_link()
        elif op == '2':
            check_links_from_file()
        elif op == '3':
            break
        else:
            print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
            time.sleep(1)

def main():
    """Fluxo principal do programa"""
    animate_cover()
    
    while True:
        opcao = show_menu()
        if opcao == '1':
            generate_links()
        elif opcao == '2':
            verify_submenu()
        elif opcao == '3':
            print(f"\n{Fore.YELLOW}Saindo...{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Opção inválida! Tente novamente.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()
