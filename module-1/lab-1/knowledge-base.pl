/**
 * # Лабораторная №1. База знаний по теме «игры».
 * Требования:
 * - [x] 20+ /1-фактов
 * - [x] 10-15 /2-фактов
 * - [x] 5-7 rules
 *
 * ## Реализация «База знаний уровней и социальных связей игроков в абстрактной игре».
 * Механика:
 * - Игроки могут быть знакомыми (друзья), что они дополнительно указывают в профиле.
 * - Игроки могут быть в команде либо во время обычной игры с другими игроками того же уровня,
 *   либо с друзьями.
 * - Во время игры с игроком большего уровня, игрок с меньшим уровнем может его увеличить.
 *
 */

% Игроки с никнеймами.
player('Denstep').
player('Landau').
player('Lesha').
player('Shaylushai').
player('Any623').
player('Le Potat').
player('Patient').
player('Pandushka').
player('Bedrosik').
player('Jorik').

% Доступные уровни в игре.
level(1).
level(2).
level(3).
level(4).
level(5).
level(6).
level(7).
level(8).
level(10).
level(11).
level(12).
level(13).
level(14).
level(15).

% Текущие достижения игроков.
has_level('Denstep', 4).
has_level('Landau', 6).
has_level('Lesha', 8).
has_level('Shaylushai', 9).
has_level('Any623', 14).
has_level('Le Potat', 8).
has_level('Patient', 11).
has_level('Pandushka', 12).
has_level('Bedrosik', 4).
has_level('Jorik', 4).

% Социальные связи в игре. (зависимости описаны в одном направлении, сверху вниз)
friends('Denstep', 'Landau').
friends('Denstep', 'Any623').
friends('Denstep', 'Patient').
friends('Denstep', 'Le Potat').

friends('Landau', 'Lesha').
friends('Landau', 'Patient').

friends('Lesha', 'Patient').
friends('Lesha', 'Shaylushai').
friends('Lesha', 'Bedrosik').

friends('Shaylushai', 'Any623').

friends('Any623', 'Le Potat').
friends('Any623', 'Pandushka').

friends('Le Potat', 'Patient').
friends('Le Potat', 'Pandushka').

friends('Bedrosik', 'Jorik').


% Проверка на коммутативную дружбу.
is_friends(P1, P2) :-
    friends(P1, P2); friends(P2, P1).

% Сравнение уровней игроков.
same_level(P1, P2) :-
    has_level(P1, L), 
    has_level(P2, L).

% Проверка возможности встретиться однажды во время матча в одной команде в ближайшей игре.
can_play_in_team(P1, P2) :-
    P1 \= P2, player(P1), player(P2),
    (same_level(P1, P2); is_friends(P1, P2)).

% Проверка возможности повысить свой уровень по средствам игры с другим игроком в ближайшей игре.
can_be_boosted_by(P1, P2) :-
    can_play_in_team(P1, P2), 
    has_level(P1, L1), 
    has_level(P2, L2), 
    L2 > L1.

% Проверка возможности однажды завести социальную связь с другим игроком в ближайшей игре.
can_become_friends(P1, P2) :-
    not(is_friends(P1, P2)), 
    can_play_in_team(P1, P2).

% Проверка возможности достичь указанного уровня в ближайшей игре.
can_get_level(P, L) :-
    level(L),
    has_level(P, OwnedLevel), OwnedLevel < L,
    player(SomePlayer),    
    can_be_boosted_by(P, SomePlayer),
    has_level(SomePlayer, SomeLevel), SomeLevel >= L.
