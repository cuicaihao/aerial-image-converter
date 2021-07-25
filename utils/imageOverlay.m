filenameImage = 'PNG/RGB.png';
I = imread(filenameImage);

filenameLabels = 'PNG/GT.png';
L = imread(filenameLabels);
classes = ["ground","building"];
ids = [0 255];

C = categorical(L,ids,classes);

B = labeloverlay(I,C);
imshow(B)
title('Original Image and Pixel Labels')

imwrite(B, 'PNG/Overlay.png');