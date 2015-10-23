function [ gamma ] = eff_test(self, I, xy)
    i = xy(1);
    j = xy(2);
    ng    = self.neighborhood(i, j);
    values = Utils.get_values(I, ng);
    'alpha'
    alpha = std(values(:))
    gamma = [];
    for y = 1:size(ng,1)
        'y'
        I(i,j)
        I(ng(y,1),ng(y, 2))
        'ng'
        ng(y,:)
        if self.distance( I(i,j), I(ng(y,1),ng(y, 2))) <= alpha
            gamma = [gamma; ng(y,:)];
        end
    end
end

