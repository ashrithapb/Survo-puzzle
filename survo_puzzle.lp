#const r = 3.
#const c = 3.

rows(1..r).
cols(1..c).

values(1..r*c).

% combinations of rows/columns are different
1 { matrix(Row, Col, Val) : values(Val) } 1 :- rows(Row), cols(Col).

% the values are different
1 { matrix(Row, Col, Val) : rows(Row),  cols(Col) } 1 :- values(Val).

% Row sums
:- #sum { Val: matrix(Row, Col, Val), values(Val), cols(Col)} != RowSum, rows(Row), rowsums(Row, RowSum).
% Col sums
:- #sum { Val: matrix(Row, Col, Val), values(Val), rows(Row)} !=ColSum, cols(Col), colsums(Col, ColSum).


#show matrix/3.