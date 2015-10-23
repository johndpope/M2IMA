classdef HyperDenoise
    %HYPERDENOISE class contains inpusif noise cancellation methods (hypergraph fashion)
    %   Detailed explanation goes here
    
    properties(Constant)
        NH
    end
    
    methods (Static)
        function Id = denoise(H, I)
            NH = HyperDenoise.noisy_hyperedges(H);
            disp('size NH')
            size(NH)
            Id = I;
            for i = 1:size(NH,1)
                %On  = HyperDenoise.open_neighborhood(H, NH(i,:));
                %ng  = I(On(:,1), On(:,2));
                %val = mean(ng(:));
                %Id(NH(i,1), NH(i,2)) = val;
                ng  = HyperDenoise.open_neighborhood(H, NH(i,:));
                if size(ng, 1) < 4
                    ng  = H.neighborhood(NH(i,1), NH(i,2));
                end
                val = Utils.get_values(I,ng);
                sor = sort(val(:));
                Id(NH(i,1), NH(i,2)) = sor(round(size(sor,1)/2));
            end
        end
        function Ep = neighbor_edge_sets(H, ng)
            Ep = H.hyper{ng(1,1), ng(1,2)};
            for y = 2:size(ng,1) 
                Ep = union(Ep, H.hyper{ng(y,1), ng(y,2)}, 'rows');
            end
        end
        function On = open_neighborhood(H, x)
            Ex = H.hyper{x(1), x(2)};
            On = HyperDenoise.neighbor_edge_sets(H, Ex);
            %On = setxor(Ep, Ex, 'rows');
        end
        function v = open_test(H, IS, x)
            On = HyperDenoise.open_neighborhood(H, IS(x, :));
            v = 0;
            for i = 1:size(On,1)
                if size(intersect(IS, On(i, :), 'rows'),1) >=1
                    v = 1;
                    break;
                end
            end
        end
        function [NH, IS] = noisy_hyperedges(H)
            IS = [];
            NH = [];
            % Determination of isolated hyperedges of H
            for i = 1:H.s_img(1)
                for j = 1:H.s_img(2)
                    Ex = H.hyper{i,j};
                    Ep = HyperDenoise.neighbor_edge_sets(H,Ex);
                    if sum(size(Ep) - size(Ex)) == 0
                        if sum(sum(Ep - Ex)) == 0
                            IS = [IS; [i,j]];
                        end
                    end
                end
            end
            % Detection of noise hyperedges
            for i = 1:size(IS, 1)
                if size(H.hyper{IS(i,1), IS(i,2)}, 1) == 1 % && not containded in thin disjoined chain
                    NH = [NH; IS(i, :)];
                end
                if HyperDenoise.open_test(H, IS, i)
                    NH = [NH; IS(i, :)];
                end
            end
        end
    end
    
end

