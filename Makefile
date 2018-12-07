# Makefile for Homework 8
SWIG_INCLUDES=-I/home/agni/opt/Anaconda3/include/python3.6m -I/home/agni/opt/Anaconda3/lib/python3.6/site-packages/numpy/core/include


swig_n:
	swig -python -c++ notch.i
	g++ -fPIC -c notch.cc notch_wrap.cxx ${SWIG_INCLUDES}
	g++ -shared notch.o notch_wrap.o ${SWIG_INCLUDES} -o _notch.so


# cleanup
clean:
	rm -f notch_c *.o *.mod *.so *.cxx 
