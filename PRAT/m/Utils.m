classdef Utils
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods(Static)
        function ng = get_values(I, neighbors)
            ng = zeros(size(neighbors,1), 1);
            for i = 1:size(neighbors,1)
                ng(i) = I(neighbors(i,1), neighbors(i,2));
            end
        end
    end
    
end

