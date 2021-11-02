import os
import sys
import argparse
import subprocess

global_ws = '131072'


if __name__ == "__main__":
    password = ''
    argparser = argparse.ArgumentParser(
        description='Set wallet on auto craking')
    argparser.add_argument('--wallets', type=str,
                           help='directory for all wallets for autowallet', required=True)
    argparser.add_argument('--passlist', type=str,
                           help='path to single wordlist', required=True)
    args = argparser.parse_args()
    input_path = args.wallets
    passlist = args.passlist
    if not os.path.isfile(passlist):
        print('The path specified does not exist')
        sys.exit()
    included_extensions = ['dat']
    file_names = os.listdir(input_path)
    for folder in file_names:
        wallet = os.path.join(input_path, folder, 'wallet.dat')
        starting = f'telegram-send --pre "Starting {wallet} with wordlist {passlist}"'
        finished = f'telegram-send --pre "Finished {wallet} with wordlist {passlist}"'
        command = f'python3 btcrecover.py --wallet {wallet} --passwordlist {passlist} --enable-opencl --dsw --enable-gpu --global-ws {global_ws}'
        subprocess.run(starting, shell=True)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        result = str(result.stdout.decode())
        if "Password found:" in result:
            sys.exit()
        subprocess.run(finished, shell=True)
print('All wallets are checked')
sys.exit()
