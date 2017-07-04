#include <Python.h>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "condor_types.h"
#include "glutils.h"

static CondorData *condor_data;

void glutils_init(CondorData *cdata) {
    condor_data = cdata;
}

GLFWwindow *glutils_init_window(int width, int height) {

    if (!glfwInit()) {
        PyErr_SetString(PyExc_RuntimeError, "GLFW Failed to initialize.");
        return NULL;
    }

    glfwWindowHint(GLFW_SAMPLES, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);

    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_COMPAT_PROFILE);

    GLFWwindow *w = glfwCreateWindow(width, height, "condor.c", NULL, NULL);

    if (w == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "GLFW Failed to open a window. "
                "Intel GPUs don't support 3.3");
        glfwTerminate();
        return NULL;
    }

    glfwMakeContextCurrent(w);
    glewExperimental = GL_TRUE;
    if (glewInit() != GLEW_OK) {
        PyErr_SetString(PyExc_RuntimeError, "GLEW Failed to initialize.");
        return NULL;
    }

    glfwSwapInterval(0);

    return w;
}

void glutils_loop(void (*loop)(void)) {
	while (!glfwWindowShouldClose(condor_data->window))
	{
        loop();
		glfwSwapBuffers(condor_data->window);
		glfwPollEvents();
	}
}

