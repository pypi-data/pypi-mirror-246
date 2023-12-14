#!/usr/bin/python

"""Functions to create some sample test games"""

import numpy as np
import argparse

import json
from pymnash.game import Game
from pymnash.util import coords_from_pos, iterindices, enumershape
from collections import defaultdict


def battle_of_genders(n):
    """A generalization of the 'battle of the sexes' game which supports any number of genders.
    The number of possible moves for each player iss equal to the total number of players.
    All players get zero payoff unless they all coordinate on a choice, each player has a particular favorite choice
    but all players get something as long as they all coordinate."""
    # We know there is one pure strategy per player, with all players playing that player's favorite.
    # There will also be one mixed  strategy for ever combination of pure strategies
    boga = np.zeros(tuple([n] * (n + 1)), dtype=float)
    #print(boga)
    for ii in range(n):
        loc = boga
        for jj in range(n):
            loc = loc[ii]
        for kk in range(n):
            if kk == ii:
                loc[kk] = n
            else:
                 loc[kk] = 1
    return Game(boga)

def reducible(n):
    """A game just to test the iterated elimination of strictly dominated strategies. """
    # 2 player version scored come from steven tadelis game theory an introduction.
    # I will extend it with obvious dominant strategies of other players.
    twoplayer = [[[4,3], [5,1], [6,2]],
                 [[2,1], [8,4], [3,6]],
                 [[3,0], [9,6], [2,8]]]
    thetuple = tuple([3, 3] + [2] * (n - 2) +  [n])
    payoffs = np.zeros(thetuple)
    for indices in iterindices(payoffs.shape):
        player = indices[len(indices) - 1]
        if player in [0, 1]:
             payoffs[indices] = twoplayer[indices[0]][indices[1]][player]
        elif indices[player] == 0:
             payoffs[indices] = 1
    return Game(payoffs)

def combo_reducible(n):
    """A game for testing iesds2. It has a strategy that is not dominated by any single other strategy
       but can be dominated by a linear combination of strategies."""
    # The game comes from steven tadelis game theory an introduction, page 115 of first edition.
    if n != 2:
        raise Exception('This game is only supported for two players')
    payoffs = [[[5, 1], [1,4], [1, 0]],
               [[3,2], [0, 0], [3, 5]],
               [[4,3], [4,4], [0,3]]]
    payoffs = np.array(payoffs)
    return Game(payoffs)



def dunderheads(n):
    """Multi-player High-Low. Similar to battle of genders, except there are only two options and all players
        have the same preferrred option."""
    # There are two pure nash equilibria, the 'smart' on where evryone picks the preferred option, and the
    # 'dunderheaded' one where everyone picks the option they don't like.
    # There should also be a 'super-dunderheaded' solutions where all player mix their picks.
    # The probability of pcking the dunderheaded option will be higher, so the higher chance of getting a match
    # exactly compensates for the lower payoff.
    payoffs = np.zeros(tuple([2] * n + [n]), dtype=float)
    for indices in iterindices(payoffs.shape):
        good = True # everyone is playing the good choice
        bad = True
        for ii in range(len(indices) - 1):
            if indices[ii] == 1: #someone is playing the bad choice
                good = False
            elif indices[ii] == 0:
                bad = False
        if good:
            payoffs[indices] = 3.0
        if bad:
            payoffs[indices] = 1.0
    return Game(payoffs)



def prisoners_dilemma(n):
    """For the multiplayer prisoner's dilemma we will say if everone cooperates then each person gets a -1 payoff.
       If exactly one player defectes he gets 0 and everyone else gets -5.
       If multiple player defect, the ones that defect get -3 and the ones that cooperate get -5.
    """
    # We will say for ever player choice '0' is cooperate and '1' is defect.
    # The innermost array is player id for payoffs
    # We know the only nash equilibrium is everybody defects.
    payoffs = np.zeros(tuple(([2] * n + [n])), dtype=float)
    for ii in range(np.prod(payoffs.shape)):
        coords = coords_from_pos(payoffs, ii)
        player = coords[ n ] # index of the player we are looking at
        he_defected = bool(coords[player])
        total_defected = sum(coords[:-1])
        if total_defected == 0:
            payoffs[coords] = -1
        elif he_defected and total_defected  == 1:
            payoffs[coords] = 0
        elif he_defected:
             payoffs[coords] = -3
        else:
             payoffs[coords] = -5
    return Game(payoffs, prisoner_labels)


def matching_pennies(n):
    """For n player matching pennies each player can choose a number in the range 0 to n -1, and player m
       wins if the result is m modulo n.
       For the 2 x 2 case think of heads as zero and tails as 1, so player 0 wins with HH or TT,
       player 1 wins with HT or TH"""
    # The obvious equilibrium is everyone plays randomly. But there are many possibilities for multiple players.
    # In the 3 player version, if 2 players
    # play randomly, the other player can play anything and it's still an equilibrium.
    # As long as at least one player is playing randomly it doesn't really matter what the
    # other players do, but just one player randomising would not be an equilibrium.
    payoffs = np.zeros(tuple([n] * (n + 1)), dtype=float)
    for ii in range(np.prod(payoffs.shape)):
        coords = coords_from_pos(payoffs, ii)
        player = coords[ n ] # index of the player we are looking at
        sum_played = sum(coords[:-1])
        if sum_played % n == player:
            payoffs[coords] = n - 1
        else:
            payoffs[coords] = -1
    #print(payoffs)
    return Game(payoffs)

def how_low_dare_you_go(n, m):
    """n players have m choices of numbers, m > n. The winning player is the player who picks
       the lowest non-negative integer not chosen by any other player."""
    # we will restrict the game to m choices so we have a hope of finding solutions.
    # In principle this game could be played with an infinite number of possible
    # moves, nobody igoing to play a number all that much higher than the number of players in any case.
    payoffs = np.zeros(tuple(([m] * n + [n])), dtype=float)
    for jj, coords in enumershape(payoffs.shape[:-1]):
        counts = defaultdict(int) # number of players picking this number
        win = None
        for iii in range(len(coords)):
            counts[coords[iii]] += 1
        for ii in sorted(counts.keys()):
            if counts[ii] == 1:
                win = ii
                break
        if win is not None:
            done = False
            for player_index in range(len(coords)):
                if coords[player_index] == win:
                    pos = list(coords)
                    pos.append(player_index)
                    payoffs[tuple(pos)] = 1
    return Game(payoffs)

def mixed_dom(n, m):
    """A two-player game where one player has a dominated strategy, but it takes a combination of
       m strategies to defat it (one player has m strategies, the other has m + 1).
       Based on a comment by kevinwangg in the thread
       https://www.reddit.com/r/GAMETHEORY/comments/18d5zxx/dominated_by_3_or_more_strategies/
    """
    if n != 2:
        raise ValueError("This game is only supported for 2 players")
    payoffs = np.zeros(tuple((m + 1, m, 2)), dtype=float)
    for ii in range(m):
        payoffs[ii][ii][0] = m + 1
        payoffs[ii][ii][1] = -1 * (m + 1)
        payoffs[m][ii][0] = 1
        payoffs[m][ii][1] = -1
    return Game(payoffs)


game_names = {"battle_of_genders":battle_of_genders, "reducible":reducible, "combo_reducible":combo_reducible,
               "dunderheads":dunderheads, "prisoners_dilemma":prisoners_dilemma, "matching_pennies":matching_pennies,
              "how_low_dare_you_go":how_low_dare_you_go, "mixed_dom":mixed_dom}

def get_game_fun(name):
    """Find the factory function based on the game name"""
    if name in game_names:
        return game_names[name]
    for game_name in game_names.keys():
        if game_name.startswith(name):
            return game_names[game_name]
    raise ValueError("Unknown game {}".format(name))

def get_canned_profile(fun, num_players):
    """Return a sample strategy profile for the game."""
    if fun == battle_of_genders:
        inner = [0] * num_players
        profile = [list(inner) for ii in range(num_players)]
        for ii in range(num_players):
            profile[ii][ii] = 1
        return profile
    if fun == dunderheads:
        aroot = 3.0 ** (1/(num_players - 1.0))
        profile = [[1 / (aroot + 1), aroot/(aroot + 1)]] * num_players
        return profile
    if fun == reducible:
        profile = [[1, 0, 0]] * 2 +  [[1, 0]] * (num_players - 2)
        return profile
    if fun == matching_pennies:
        frac = 1 / num_players
        profile = [[frac] * num_players,
                   [frac] * num_players] + [[1] + [0] * (num_players - 1)] * (num_players - 2)
        return profile

    raise Exception("Unsupported")

if __name__ == '__main__':
    from argparse import ArgumentParser
    from ast import literal_eval
    parser = ArgumentParser()
    parser.add_argument('--players', help = "number of players", type=int, default=3)
    parser.add_argument('--m', type=int, default=None, help="integer parameter that exists for some games")
    parser.add_argument('--game', help="game name", default='battle_of_genders')
    parser.add_argument('--pure', action='store_true', help='find pure strategy equilibria')
    parser.add_argument('--payoffs', help='show payoff matrix', action='store_true')
    parser.add_argument('--profile', help='test if profile is equilibrium')
    parser.add_argument('--canned', help='test if canned profile is equilibrium', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--iesds', action='store_true')
    parser.add_argument('--combo', action='store_true', help='check if a combo of strategies dominates a strategy')
    parser.add_argument('--support', help='try to find nash equilibria with the given support', default = None)
    parser.add_argument('--all', help='try to find all nash equilibria for this game', action='store_true')
    args = parser.parse_args()
    agame = None
    profile = None
    game_fun = get_game_fun(args.game)
    if game_fun in [how_low_dare_you_go, mixed_dom]:
        agame = game_fun(args.players, args.m)
    else:
        agame = game_fun(args.players)

    if args.payoffs:
        print('payoffs:')
        print(repr(agame.payoffs))
        print('')
    if args.pure:
        print('pure:')
        print(repr(agame.find_pure()))
    if args.canned:
        profile = get_canned_profile(game_fun, args.players)
        print('profile:')
        print(profile)
        is_nash = agame.is_nash(profile)
        print('is_nash:', is_nash)
    if args.profile:
        profile = literal_eval(args.profile)
        print('profile:')
        print(profile)
        is_nash = agame.is_nash(profile)
        print('is_nash:', is_nash)
    if args.iesds:
        agame.iesds()
        print('dominated strategies:')
        print(agame.dominated)
    if args.combo:
        thecombo = literal_eval(args.combo)
        print(agame._combo_dominates(1, 0, 1, 2))
    if args.support:
        support = literal_eval(args.support)
        indifference_probs = agame._get_indifference_probs(support)
        print('support:')
        print(support)
        print('indifference probs:')
        print(indifference_probs)
    if args.all:
        all_nash = agame.find_all_equilibria()
        for anash in all_nash:
            print(anash)

#./test_sample_game.py --game battle --support "[[0,1,2], [0,1,2], [0,1,2]]" # this will give unique probs
#./test_sample_game.py --game battle --support "[[1,2], [1,2], [1,2]]"
#./test_sample_game.py --game battle --players 4 --support "[[1,2], [1,2], [0,3], [0, 3]]" # this should give lines of solutions.
