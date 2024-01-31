
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img, output_img;
  int i,j;

  if ( argc != 2 ) error( argv[0] );

  /* open image file */
  if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file %s\n", argv[1] );
    exit ( 1 );
  }

  /* read image */
  if ( read_TIFF ( fp, &input_img ) ) {
    fprintf ( stderr, "error reading file %s\n", argv[1] );
    exit ( 1 );
  }

  /* close image file */
  fclose ( fp );

  /* check the type of image data */
  if ( input_img.TIFF_type != 'c' ) {
    fprintf ( stderr, "error:  image must be 24-bit color\n" );
    exit ( 1 );
  }

  /* set up structure for output color image */
  /* Note that the type is 'c' rather than 'g' */
  get_TIFF ( &output_img, input_img.height, input_img.width, 'c' );

  /* Apply filter h(m, n) = 1/81*/
  for ( i = 4; i < input_img.height - 4; i++)
  for ( j = 4; j < input_img.width - 4; j++) {
    int red = 0;
    int green = 0;
    int blue  = 0;
    for (int n = -4; n <= 4; n++)
    for (int m = -4; m <= 4; m++) {
        red += input_img.color[0][i+m][j+n];
        green += input_img.color[1][i+m][j+n];
        blue += input_img.color[2][i+m][j+n];
    }
   
    output_img.color[0][i][j] = red / 81;
    output_img.color[1][i][j] = green / 81;
    output_img.color[2][i][j] = blue / 81;
  }

  /* open output image file */
  if ( ( fp = fopen ( "lpf_output.tif", "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file lpf_output.tif\n");
    exit ( 1 );
  }

  /* write output image */
  if ( write_TIFF ( fp, &output_img ) ) {
    fprintf ( stderr, "error writing TIFF file %s\n", argv[2] );
    exit ( 1 );
  }

  /* close output image file */
  fclose ( fp );

  /* de-allocate space which was used for the images */
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

