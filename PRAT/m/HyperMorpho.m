classdef HyperMorpho
    %HYPERMORPHO Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        strel  = 1;
        result 
    end
    
    methods
        function Hm = HyperMorpho(se)
            Hm.strel  = se;
        end
        function delta = hyperdilate(self, H)
            delta = 0;
        end
        function epsilon = hypererode(self, H)
            epsilon = 0;
        end
        function open = hyperopen(self, H)
            open = 0;
        end
        function close = hyperclose(self, H)
            close = 0;
        end
    end
    
end

