import math
import hashlib
import json
from time import time

from colorama import init, Fore, Style


init()

class Blockchain(object):
    def __init__(self):
        self.amount = 0
        self.current_transactions = []
        self.chain = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):

        proof = 0
        frash = 0
        while self.valid_proof(last_proof, proof, frash)[0] is False:
            proof += 1
            frash = math.sqrt(last_proof)

        return [proof, self.valid_proof(last_proof, proof, frash)[1]]

    @staticmethod
    def valid_proof(last_proof, proof, frash):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(Fore.GREEN, guess_hash)
        return [guess_hash[:4] == "0000", guess_hash]

    def maining(self):
        try:
            while True:
                print(Style.RESET_ALL)
                m = self.proof_of_work(self.chain[-1]['proof'])
                if m:
                    self.amount += 1
                    self.new_transaction('codeby@inmail.onion', 'cryptochain@cryptmail.in', self.amount)
                    self.new_block(m[0], m[1])
                    #print(int(self.chain[-1]['proof']))
        except KeyboardInterrupt:
            print(Fore.CYAN, self.chain)


if __name__ == '__main__':
    b = Blockchain()
    b.maining()
