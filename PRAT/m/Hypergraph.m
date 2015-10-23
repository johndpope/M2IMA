classdef Hypergraph
    %HYPERGRAPH construction class (IANH fashion)
    %   Detailed explanation goes here
    
    properties
        hyper
        s_img
    end
    
    methods
        function H = Hypergraph(p_img)
            [l,c] = size(p_img);
            H.s_img   = [l,c];
            H.hyper = cell(l,c);
            for i = 1:l
                for j = 1:c
                    H.hyper{i,j} = H.get_effective_neighbors(p_img, [i,j]);
                end
            end
        end
        function d = distance(self, p_a, p_b)
            d = abs(double(p_a) - double(p_b));
        end
        function ng = neighborhood(self, p_i, p_j)
            i1=mod(p_i-2,self.s_img(1))+1;
            i2=mod(p_i,self.s_img(1))+1;
            j1=mod(p_j-2,self.s_img(2))+1;
            j2=mod(p_j,self.s_img(2))+1;
            ng=[i1 i1 i1 p_i p_i p_i i2 i2 i2; j1 p_j j2 j1 p_j j2 j1 p_j j2 ]';
        end
        function gamma = get_effective_neighbors(self, I, xy)
            i = xy(1);
            j = xy(2);
            ng    = self.neighborhood(i, j);
            values = Utils.get_values(I, ng);
            alpha = std(values(:));
            gamma = [];
            for y = 1:size(ng,1)
                if self.distance( I(i,j), I(ng(y,1),ng(y, 2))) <= alpha
                    gamma = [gamma; ng(y,:)];
                end
            end
        end
    end
    
end

