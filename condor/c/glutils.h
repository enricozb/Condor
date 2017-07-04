#ifndef __GLUTILS_C__
#define __GLUTILS_C__

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "condor_types.h"

// Sets up reference to useful CondoData structure
void glutils_init(CondorData*);

// Initializes window and modifies condor_data
GLFWwindow *glutils_init_window(int width, int height);

// Begins main drawing loop
void glutils_loop(void (*loop)(void));

#endif // __GLUTILS_C__

