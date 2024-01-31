
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void error(char *name);
double clip(double px);

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

  /* Apply filter g(m, n) = 1 + 1.5(1 - 1/25x)*/
  for ( i = 2; i < input_img.height - 2; i++)
  for ( j = 2; j < input_img.width - 2; j++) {
    int red = 0;
    int green = 0;
    int blue  = 0;
    for (int n = -2; n <= 2; n++)
    for (int m = -2; m <= 2; m++) {
        red += input_img.color[0][i+m][j+n];
        green += input_img.color[1][i+m][j+n];
        blue += input_img.color[2][i+m][j+n];
    }

    int temp_red = input_img.color[0][i][j] + 1.5 * (input_img.color[0][i][j] - red/25);
    int temp_green = input_img.color[1][i][j] + 1.5 * (input_img.color[1][i][j] - green/25);
    int temp_blue = input_img.color[2][i][j] + 1.5 * (input_img.color[2][i][j] - blue/25);

    output_img.color[0][i][j] = clip(temp_red);
    output_img.color[1][i][j] = clip(temp_green);
    output_img.color[2][i][j] = clip(temp_blue);
  }

  /* open output image file */
  if ( ( fp = fopen ( "sf_output.tif", "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file sf_output.tif\n");
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
    printf("It then writes out the sherpened image\n");
    printf("with the name 'sf_output.tiff'.\n");
    exit(1);
}

double clip(double px)
{
  if (px > 255)  return 255;
  if (px < 0)  return 0;
  return px;
}