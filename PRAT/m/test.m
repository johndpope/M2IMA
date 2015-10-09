I = imread('109703.jpg');
Ig = padarray(double(rgb2gray(I)), [1 1]);
%imshow(Ig);
H = build_INAH(Ig);
