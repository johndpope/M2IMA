function [ If ] = median( I )
%MEDIAN Summary of this function goes here
%   Detailed explanation goes here

If =  I;
[l,c] = size(If);
for i = 1:l
    for j = 1:c
        i1=mod(i-2, l)+1;
        i2=mod(i,l)+1;
        j1=mod(j-2,c)+1;
        j2=mod(j,c)+1;
        ng=[i1 i1 i1 i i i i2 i2 i2; j1 j j2 j1 j j2 j1 j j2 ]';
        v = If(ng(:,1), ng(:,2));
        s = sort(v(:));
        If(i,j) = s(round(size(s,1)/2));
    end
end
end

