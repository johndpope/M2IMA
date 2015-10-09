function [ISO,NH,IS] = hyper_noisy(H)
ISO = cell(size(H,1),1);
NH  = cell(size(H,1),1);
IS  = cell(size(H,1),1);
%Determination of isolated hypergraphs of H
for i=1:size(H{2},2)-1
    Ey = other_hyperedges(H, i);
    if Ey == H{2}{i}
        if size(H{2}{i},2) == 1
            ISO{i} = H{2}{i};
        else
            IS{i} = H{2}{i};
        end
    end
end
%Detection of noise hyperedges of H
disp 'iso'
size(ISO)
for i=1:size(ISO, 1)
    for j=i+1:size(ISO,1)
        for k=j+1:size(ISO,1)
            if not_neighbors(H, i, j) && not_neighbors(H, i, k)  && not_neighbors(H, j, k)
                NH{i} = H{2}{i};
            end
        end
    end
end
for i=1:size(IS,1)
    if neigX_in_ISO_or_IS(H, i)
        NH{i} = H{2}{i};
    end
end
end

function Ey = other_hyperedges(H, x)
    Ey = {};
    for y=1:size(H{2}{x},2)
        cord = H{2}{x}{y};
        Ey   = H{2}{(cord(1)-1)};
        for iso=1:size(ISO, 1)
            if 
    end
end