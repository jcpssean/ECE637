
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
  double **red,**green, **blue;
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

  /* Allocate image of double precision floats */
  red = (double **)get_img(input_img.width,input_img.height,sizeof(double));
  green = (double **)get_img(input_img.width,input_img.height,sizeof(double));
  blue = (double **)get_img(input_img.width,input_img.height,sizeof(double));

  /* copy red component to double array */
  for ( i = 0; i < input_img.height; i++ )
  for ( j = 0; j < input_img.width; j++ ) {
    red[i][j] = input_img.color[0][i][j];
  }

  /* copy green component to double array */
  for ( i = 0; i < input_img.height; i++ )
  for ( j = 0; j < input_img.width; j++ ) {
    green[i][j] = input_img.color[1][i][j];
  }

  /* copy blue component to double array */
  for ( i = 0; i < input_img.height; i++ )
  for ( j = 0; j < input_img.width; j++ ) {
    blue[i][j] = input_img.color[2][i][j];
  }

  /* set up structure for output color image */
  /* Note that the type is 'c' rather than 'g' */
  get_TIFF ( &output_img, input_img.height, input_img.width, 'c' );

  /* Apply IIR filter starting at [1][1]*/
  for ( i = 1; i < input_img.height; i++ )
  for ( j = 1; j < input_img.width; j++ ) {
    red[i][j] = 0.01*input_img.color[0][i][j] + 0.9*red[i][j-1] + 0.9*red[i-1][j] - 0.81*red[i-1][j-1];
    green[i][j] = 0.01*input_img.color[1][i][j] + 0.9*green[i][j-1] + 0.9*green[i-1][j] - 0.81*green[i-1][j-1];
    blue[i][j] = 0.01*input_img.color[2][i][j] + 0.9*blue[i][j-1] + 0.9*blue[i-1][j] - 0.81*blue[i-1][j-1];
    }

  for ( i = 0; i < input_img.height; i++ )
  for ( j = 0; j < input_img.width; j++ ) {
    output_img.color[0][i][j] = clip(red[i][j]);
    output_img.color[1][i][j] = clip(green[i][j]);
    output_img.color[2][i][j] = clip(blue[i][j]);
  }

  /* open output image file */
  if ( ( fp = fopen ( "iir_output.tif", "wb" ) ) == NULL ) {
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