import requests
import json
import time
import sys
import random
import subprocess
import string
from colorama import init, Fore, Style

init()  # Initialize colorama

def animate_cover():
    sys.stdout.write("""
    █████████╗██╗   ██╗██████╗ ██████╗ 
    ╚══██╔══╝██║   ██║██╔══██╗██╔══██╗
       ██║   ██║   ██║██████╔╝██║  ██║
       ██║   ██║   ██║██╔═══╝ ██║  ██║
       ██║   ╚██████╔╝██║     ██████╔╝
       ╚═╝    ╚═════╝ ╚═╝     ╚═════╝ 
    """)
    sys.stdout.write("\n")
    sys.stdout.write("NitroChecker")
    sys.stdout.write("\n")
    sys.stdout.write("Loading")
    start_time = time.time()
    stop_time = start_time + random.uniform(3, 6)

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
    time.sleep(1)

def send_webhook(url, content):
    data = {
        "content": content
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            print(f"{Fore.GREEN}[WEBHOOK SENT]{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[WEBHOOK WARNING] Status: {response.status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[WEBHOOK ERROR] {e}{Style.RESET_ALL}")

def generate_nitro_code():
    """Gera um código de Nitro aleatório no formato: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"""
    # Formato: 24 caracteres hexadecimais no formato de gift code do Discord
    
    def random_hex(length):
        return ''.join(random.choices('0123456789abcdef', k=length))
    
    code = f"{random_hex(8)}-{random_hex(4)}-{random_hex(4)}-{random_hex(4)}-{random_hex(12)}"
    return code

def generate_nitro_codes():
    """Função para gerar múltiplos códigos Nitro"""
    print(f"\n{Fore.CYAN}=== GERADOR DE LINKS NITRO ==={Style.RESET_ALL}")
    
    while True:
        try:
            num_codes = int(input("Quantos links de Nitro você quer gerar? "))
            if num_codes <= 0:
                print(f"{Fore.RED}Por favor, digite um número positivo.{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido.{Style.RESET_ALL}")
    
    # Nome do arquivo para salvar
    filename = input("Nome do arquivo para salvar os links (padrão: Nitro Codes.txt): ").strip()
    if not filename:
        filename = "Nitro Codes.txt"
    
    # Gerar códigos
    codes = []
    print(f"\n{Fore.YELLOW}Gerando {num_codes} códigos...{Style.RESET_ALL}")
    
    for i in range(num_codes):
        code = generate_nitro_code()
        codes.append(code)
        # Feedback visual
        print(f"{Fore.CYAN}[{i+1}/{num_codes}]{Style.RESET_ALL} {code}")
        time.sleep(0.1)  # Pequena pausa para efeito visual
    
    # Salvar no arquivo
    with open(filename, "w") as file:
        for code in codes:
            file.write(f"{code}\n")
    
    print(f"\n{Fore.GREEN}[SUCESSO]{Style.RESET_ALL} {num_codes} links salvos em '{filename}'")
    print(f"\nDica: Você pode verificar estes links na opção 2 do menu principal.")
    
    input(f"\nPressione Enter para voltar ao menu...")

def check_single_code():
    """Verifica um único código Nitro"""
    print(f"\n{Fore.CYAN}=== VERIFICAR UM LINK ==={Style.RESET_ALL}")
    
    code = input("Digite o código Nitro para verificar: ").strip()
    
    if not code:
        print(f"{Fore.RED}Nenhum código digitado.{Style.RESET_ALL}")
        return
    
    webhook_url = input("Digite a URL do webhook do Discord (ou Enter para pular): ").strip()
    
    print(f"\n{Fore.YELLOW}Verificando código: {code}{Style.RESET_ALL}")
    
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = f"{Fore.GREEN}[VALID]{Style.RESET_ALL} {code}"
            print(result)
            
            if webhook_url:
                send_webhook(webhook_url, result)
            
            # Salvar código válido
            with open("Valid_Codes.txt", "a") as file:
                file.write(f"{code}\n")
            print(f"{Fore.GREEN}Código salvo em Valid_Codes.txt{Style.RESET_ALL}")
            
        elif response.status_code == 429:
            print(f"{Fore.RED}[RATE LIMITED]{Style.RESET_ALL} Muitas requisições. Aguarde um momento.")
        else:
            print(f"{Fore.RED}[INVALID]{Style.RESET_ALL} {code} (Status: {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Falha na conexão: {e}")
    
    input(f"\nPressione Enter para voltar ao menu...")

def check_nitro_code(code, webhook_url, valid_file):
    """Verifica um código Nitro individual e retorna se é válido"""
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            result = f"{Fore.GREEN}[VALID]{Style.RESET_ALL} {code}"
            print(result)
            if webhook_url:
                send_webhook(webhook_url, result)
            valid_file.write(f"{code}\n")
            return True
        elif response.status_code == 429:
            result = f"{Fore.YELLOW}[RATE LIMITED]{Style.RESET_ALL} Aguardando... {code}"
            print(result)
            time.sleep(5)  # Espera 5 segundos antes de continuar
            return False
        else:
            result = f"{Fore.RED}[INVALID]{Style.RESET_ALL} {code}"
            print(result)
            return False
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Falha ao verificar {code}: {e}")
        return False

def check_nitro_codes_from_file():
    """Verifica códigos Nitro a partir de um arquivo"""
    print(f"\n{Fore.CYAN}=== VERIFICAR LINKS DE ARQUIVO ==={Style.RESET_ALL}")
    
    # Perguntar sobre o arquivo
    has_file = input("Você já tem um arquivo com códigos? (s/n): ").strip().lower()
    
    if has_file == 's':
        print(f"\nArquivos disponíveis no diretório atual:")
        import os
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
        if txt_files:
            for i, file in enumerate(txt_files, 1):
                print(f"  {Fore.CYAN}[{i}]{Style.RESET_ALL} {file}")
            print(f"  {Fore.CYAN}[0]{Style.RESET_ALL} Digitar nome manualmente")
            
            choice = input("\nEscolha o número do arquivo: ").strip()
            
            if choice == '0':
                file_path = input("Digite o nome do arquivo: ").strip()
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(txt_files):
                        file_path = txt_files[idx]
                    else:
                        print(f"{Fore.RED}Opção inválida.{Style.RESET_ALL}")
                        return
                except ValueError:
                    print(f"{Fore.RED}Opção inválida.{Style.RESET_ALL}")
                    return
        else:
            file_path = input("Digite o nome do arquivo com os códigos: ").strip()
    else:
        print(f"\nVocê pode:")
        print(f"1. Usar a opção 1 do menu para gerar códigos")
        print(f"2. Criar um arquivo .txt com os códigos (um por linha)")
        file_path = input("\nDigite o nome do arquivo de códigos: ").strip()
    
    # Verificar se o arquivo existe
    if not os.path.exists(file_path):
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} Arquivo '{file_path}' não encontrado!")
        return
    
    # Ler arquivo
    try:
        with open(file_path, "r") as file:
            nitro_codes = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} Falha ao ler arquivo: {e}")
        return
    
    num_codes = len(nitro_codes)
    print(f"\n{Fore.CYAN}{num_codes} códigos encontrados em '{file_path}'{Style.RESET_ALL}")
    
    if num_codes == 0:
        print(f"{Fore.YELLOW}Nenhum código encontrado no arquivo.{Style.RESET_ALL}")
        return
    
    # Configurar webhook
    use_webhook = input("\nDeseja enviar resultados para um webhook do Discord? (s/n): ").strip().lower()
    webhook_url = ""
    if use_webhook == 's':
        webhook_url = input("Digite a URL do webhook: ").strip()
    elif use_webhook == 'n':
        webhook_url = "nom" # Só pra ele não mandar webhook mesmo
    
    # Confirmar
    print(f"\n{Fore.YELLOW}Pressione Enter para iniciar a verificação...{Style.RESET_ALL}")
    input()
    
    valid_codes = []
    
    with open("Valid_Codes.txt", "w") as valid_file:
        for i, code in enumerate(nitro_codes, 1):
            print(f"{Fore.CYAN}[{i}/{num_codes}]{Style.RESET_ALL}", end=" ")
            if check_nitro_code(code, webhook_url, valid_file):
                valid_codes.append(code)
            # Pequena pausa para evitar rate limiting
            time.sleep(0.5)
    
    valid_count = len(valid_codes)
    invalid_count = num_codes - valid_count

    print(f"\n{Fore.GREEN}=== RESULTADOS ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}Válidos: {valid_count}{Style.RESET_ALL}")
    print(f"{Fore.RED}Inválidos: {invalid_count}{Style.RESET_ALL}")
    
    if valid_count > 0:
        print(f"\n{Fore.GREEN}Códigos válidos salvos em 'Valid_Codes.txt'{Style.RESET_ALL}")
    
    input(f"\nPressione Enter para voltar ao menu...")

def main_menu():
    """Menu principal do programa"""
    while True:
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)
        
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}  NITRO CHECKER & GENERATOR{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  1.{Style.RESET_ALL} {Fore.GREEN}Gerar links Nitro{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  2.{Style.RESET_ALL} {Fore.BLUE}Verificar links{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  3.{Style.RESET_ALL} {Fore.RED}Sair{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        choice = input(f"{Fore.WHITE}Escolha uma opção (1-3): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            generate_nitro_codes()
        elif choice == '2':
            verify_menu()
        elif choice == '3':
            print(f"\n{Fore.YELLOW}Saindo...{Style.RESET_ALL}")
            time.sleep(1)
            sys.exit(0)
        else:
            print(f"{Fore.RED}Opção inválida! Tente novamente.{Style.RESET_ALL}")
            time.sleep(1)

def verify_menu():
    """Submenu para verificação de links"""
    import os
    
    while True:
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)
        
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  VERIFICAR LINKS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  1.{Style.RESET_ALL} {Fore.GREEN}Verificar um link{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  2.{Style.RESET_ALL} {Fore.YELLOW}Verificar links de arquivo{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  3.{Style.RESET_ALL} {Fore.RED}Voltar ao menu principal{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        choice = input(f"{Fore.WHITE}Escolha uma opção (1-3): {Style.RESET_OUT}").strip()
        
        if choice == '1':
            check_single_code()
        elif choice == '2':
            check_nitro_codes_from_file()
        elif choice == '3':
            break
        else:
            print(f"{Fore.RED}Opção inválida! Tente novamente.{Style.RESET_ALL}")
            time.sleep(1)

# Início do programa
if __name__ == "__main__":
    import os
    animate_cover()
    main_menu()
