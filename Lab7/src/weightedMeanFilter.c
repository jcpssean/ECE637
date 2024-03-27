#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void error(char *name);

void swap(double *a, double *b){
	int temp = *a;
	*a = *b;
	*b = temp;
}

void sort(double arr1[], double arr2[], int n){
	for (int i=0; i<n-1; i++){
		for (int j=0; j<n-i-1; j++){
			if (arr1[j] < arr1[j+1]){
				swap(&arr1[j], &arr1[j+1]);
				swap(&arr2[j], &arr2[j+1]);
			}
		}
	}
}

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img, output_img;
  double **img, **img_padded;
	int32_t i, j, a, b, idx;
	double sum1, sum2;
	double X[25];
	double weight[25] = {1, 1, 1, 1, 1,
                       1, 2, 2, 2, 1,
                       1, 2, 2, 2, 1,
                       1, 2, 2, 2, 1,
                       1, 1, 1, 1, 1};
  
  char *input_file = "img14sp.tif";

  /* open image file */
  if ( ( fp = fopen ( input_file, "rb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file %s\n", input_file );
    exit ( 1 );
  }

  /* read image */
  if ( read_TIFF ( fp, &input_img ) ) {
    fprintf ( stderr, "error reading file %s\n", input_file );
    exit ( 1 );
  }

  /* close image file */
  fclose ( fp );

  /* check the type of image data */
  if ( input_img.TIFF_type != 'g' ) {
    fprintf ( stderr, "error:  image must be 24-bit color\n" );
    exit ( 1 );
  }

  /* set up structure for output grey image */
  /* Note that the type is 'g' rather than 'c' */
  get_TIFF ( &output_img, input_img.height, input_img.width, 'g' );

  /* Allocate image and a padded image */
	img = (double **)get_img(input_img.width, input_img.height, sizeof(double));
	img_padded = (double **)get_img(input_img.width+4, input_img.height+4, sizeof(double));

  /* Pad image */
	for (i=0; i<input_img.height+2; i++){
    for (j=0; j<input_img.width+2; j++){
      img_padded[i][j] = 0;
    }
	}

  for (i=0; i<input_img.height; i++){
    for (j=0; j<input_img.width; j++){
      img_padded[i+2][j+2] = input_img.mono[i][j];
    }
	}


  for (i=2; i<input_img.height+2; i++){
		for (j=2; j<input_img.width+2; j++){
			idx = 0;
			for (a=i-2; a<=i+2; a++){
				for (b=j-2; b<=j+2; b++){
					X[idx] = img_padded[a][b];
					idx += 1;
				}
			}

			sort(X, weight, sizeof(X)/sizeof(X[0]));

			/* Find median index a*/
			idx = 1;
			sum1 = 0;
			sum2 = 0;
			while(1) {
				for (b=0; b<=idx; b++){
					sum1 = sum1 + weight[b];
				}
				for (b=idx+1; b<sizeof(weight)/sizeof(weight[0]); b++){
					sum2 = sum2 + weight[b];
				}
				if (sum1 >= sum2) {
					break;
				}
				sum1 = 0;
				sum2 = 0;
				idx += 1;
			}

			img[i-2][j-2] = X[idx];
		}
	}

  for (i=0; i<input_img.height; i++){
		for (j=0; j<input_img.width; j++){
			// pixel = (int32_t)img[i][j];
			if(img[i][j] > 255) {
				img[i][j] = 255;
			}
			if(img[i][j]<0) {
				img[i][j] = 0;
			}
			output_img.mono[i][j] = (int32_t)img[i][j];
		}
	}
  

  /* open output image file */
  if ( ( fp = fopen ( "wmf_sp.tif", "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file wmf_sp.tif\n");
    exit ( 1 );
  }

  /* write output image */
  if ( write_TIFF ( fp, &output_img ) ) {
    fprintf ( stderr, "error writing TIFF file wmf_sp.tif\n");
    exit ( 1 );
  }

  /* close output image file */
  fclose ( fp );

  /* de-allocate space which was used for the images */
  free_img((void *)img);
  free_img((void *)img_padded);
  free_TIFF ( &(input_img) );
  free_TIFF ( &(output_img) ); 

  return(0);
}

void error(char *name)
{
    printf("usage:  %s  image.tiff \n\n",name);
    printf("this program reads in a 24-bit color TIFF image.\n");
    printf("It then pass the input image through a low pass filter,\n");
    printf("and writes out the result as an 8-bit image\n");
    printf("with the name 'lpf_output.tiff'.\n");
    exit(1);
}

