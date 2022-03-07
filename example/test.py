import random
import time
def subsequenceCount(s1, s2):
    dp = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
    for i in range(1, len(s1) + 1):
        c1 = s1[i - 1]
        for j in range(1, len(s2) + 1):
            c2 = s2[j - 1]
            if c1 == c2:
                if i == 1:
                    dp[i][j] = dp[i][j - 1] + 1
                else:
                    dp[i][j] = dp[i][j - 1] + dp[i - 1][j - 1]
            else:
                dp[i][j] = dp[i][j - 1]
    for lin in dp:
        print(lin)
    return dp[-1][-1]

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# print(factorial(60)) # 5! = 120
# print(subsequenceCount("ABC", "ABCBABC"))
# def main():
#     print(subsequenceCount("ABC", "ABCBABC"))
#
#
# if __name__ == '__main__':
#     main()

# class Card:
#     def __init__(self):
#         self.cardNum = "No num"
#         self.cardSuit = "No suit"
#     def __init__(self, cardNum, cardSuit):
#         self.cardNum = cardNum
#         self.cardSuit = cardSuit
#     def __str__(self):
#         return "This card is the " + self.cardNum + " of " + self.cardSuit
#
#     def shuffleSuit(self):
#         suit_to_choose = ["Diamond", "Club", "Heart", "Spade"]
#         suit_to_choose.remove(self.cardSuit) #prevents shuffling to same thing
#         self.cardSuit = random.choice(suit_to_choose)
#
# cards = [Card("1", "Heart"), Card("J", "Spade"), Card("Q", "Heart")]
#
#
# for card in cards:
#     print("Before shuffle:", card)
#     card.shuffleSuit()
#     print("Post shuffle:", card)

# def example():
#     def changeColor():
#         print("I changed colors!")
#     def changeSpeed():
#         print("I changed speeds!")
#     def addOrRemove():
#         print("I added or removed!")
#     while True:
#         changeColor()
#         changeSpeed()
#         addOrRemove()
#         time_waited = random.randrange(5)
#         time.sleep(time_waited)
#         print("I waited {} seconds!".format(time_waited))
# example()

# this represents y = x + 10
def function_y(x):
    return 10 + x

#let input_array be of form [1,2,3,...,etc]
def example(input_array):
    ret_array = []
    for x in input_array:
        ret_array.append(function_y(x))
    return ret_array

'''

input_array = [1,2,3]
example(input_array)
output: [11, 12, 13]

'''
