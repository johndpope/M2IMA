I  = imread('../images/sahara.jpg');
I  = rgb2gray(I);
In = imnoise(I, 'salt & pepper', 0.02);
H  = Hypergraph(In);
Id = HyperDenoise.denoise(H,In);
%Ic = HyperDenoise.denoise(H,In);

figure();
subplot(1,3,1);
imshow(I, 'border', 'tight');
title('original');
subplot(1,3,2);
imshow(In, 'border', 'tight');
title('Noise');
subplot(1,3,3);
imshow(Id, 'border', 'tight');
title('Noise detection');

%aux = [13 19 19 18; 14 10 10 18; 15 10 10 13; 14 10 10 10; 15 14 15 15]';


