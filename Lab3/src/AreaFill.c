#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"
#include "connectedNeighbors.h"

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img, output_img;
  
  char *input_file = "img22gd2.tif";

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

  // allocate seg
  unsigned int **seg = (unsigned int **)get_img(input_img.width, input_img.height, sizeof(unsigned int*));
  int numConPixels = 0;
  struct pixel s = {.m = 67, .n = 45};
  double T = 3;
  int classLabel = 1;

  // initialize seg
  for (int i = 0; i < input_img.height; i++)
  for (int j = 0; j < input_img.width; j++) {
    seg[i][j] = 0;
  }

  ConnectedSet(s, T, input_img.mono, input_img.width, input_img.height, classLabel, seg, &numConPixels);

  // convert to binary image
  for (int i = 0; i < input_img.height; i++)
  for (int j = 0; j < input_img.width; j++) {
    if (seg[i][j] == classLabel) {
        output_img.mono[i][j] = 0;
    } else {
        output_img.mono[i][j] = 255;
    }
  }
  

  /* open output image file */
  if ( ( fp = fopen ( "connected_output_3.tif", "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file connected_output.tif\n");
    exit ( 1 );
  }

  /* write output image */
  if ( write_TIFF ( fp, &output_img ) ) {
    fprintf ( stderr, "error writing TIFF file connected_output.tif\n");
    exit ( 1 );
  }

  /* close output image file */
  fclose ( fp );

  /* de-allocate space which was used for the images */
  free_img((void *)seg);
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

