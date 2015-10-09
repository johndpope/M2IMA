function [H] = build_INAH(I)
[n,m] = size(I);
X = {{}};
E = {{}};
for i = 2:n-1
    for j = 2:m-1
        alpha = std([I(i,j), I(i-1,j-1), I(i-1,j), I(i,j-1), I(i+1,j-1), I(i+1, j), I(i-1, j+1), I(i, j+1)]);
        gamma = {};
        for x = -1:1:1
            for y = -1:1:1
                if distance(I(i,j), I(i+x,j+y)) <= alpha
                    gamma{end+1} = [i+x,j+y];
                end
            end
        end
        X{end}{end+1} = [i,j];
        E{end}{end+1} = gamma;
    end
    X{end+1} = {};
    E{end+1} = {};
end
H = {X, E};
end

function d = distance(a, b)
    d = abs(a-b);
end