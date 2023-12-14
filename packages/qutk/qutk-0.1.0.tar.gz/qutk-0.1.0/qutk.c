



#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif 
#if defined(CYTHON_LIMITED_API) && 0
  #ifndef Py_LIMITED_API
    #if CYTHON_LIMITED_API+0 > 0x03030000
      #define Py_LIMITED_API CYTHON_LIMITED_API
    #else
      #define Py_LIMITED_API 0x03030000
    #endif
  #endif
#endif

#include "Python.h"
#ifndef Py_PYTHON_H
    #error Python headers needed to compile C extensions, please install development version of Python.
#elif PY_VERSION_HEX < 0x02070000 || (0x03000000 <= PY_VERSION_HEX && PY_VERSION_HEX < 0x03030000)
    #error Cython requires Python 2.7+ or Python 3.3+.
#else
#if defined(CYTHON_LIMITED_API) && CYTHON_LIMITED_API
#define __PYX_EXTRA_ABI_MODULE_NAME "limited"
#else
#define __PYX_EXTRA_ABI_MODULE_NAME ""
#endif
#define CYTHON_ABI "3_0_6" __PYX_EXTRA_ABI_MODULE_NAME
#define __PYX_ABI_MODULE_NAME "_cython_" CYTHON_ABI
#define __PYX_TYPE_MODULE_PREFIX __PYX_ABI_MODULE_NAME "."
#define CYTHON_HEX_VERSION 0x030006F0
#define CYTHON_FUTURE_DIVISION 1
#include <stddef.h>
#ifndef offsetof
  #define offsetof(type, member) ( (size_t) & ((type*)0) -> member )
#endif
#if !defined(_WIN32) && !defined(WIN32) && !defined(MS_WINDOWS)
  #ifndef __stdcall
    #define __stdcall
  #endif
  #ifndef __cdecl
    #define __cdecl
  #endif
  #ifndef __fastcall
    #define __fastcall
  #endif
#endif
#ifndef DL_IMPORT
  #define DL_IMPORT(t) t
#endif
#ifndef DL_EXPORT
  #define DL_EXPORT(t) t
#endif
#define __PYX_COMMA ,
#ifndef HAVE_LONG_LONG
  #define HAVE_LONG_LONG
#endif
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#ifndef Py_HUGE_VAL
  #define Py_HUGE_VAL HUGE_VAL
#endif
#define __PYX_LIMITED_VERSION_HEX PY_VERSION_HEX
#if defined(GRAALVM_PYTHON)
  
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_LIMITED_API 0
  #define CYTHON_COMPILING_IN_GRAAL 1
  #define CYTHON_COMPILING_IN_NOGIL 0
  #undef CYTHON_USE_TYPE_SLOTS
  #define CYTHON_USE_TYPE_SLOTS 0
  #undef CYTHON_USE_TYPE_SPECS
  #define CYTHON_USE_TYPE_SPECS 0
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #if PY_VERSION_HEX < 0x03050000
    #undef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 0
  #elif !defined(CYTHON_USE_ASYNC_SLOTS)
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #undef CYTHON_USE_UNICODE_INTERNALS
  #define CYTHON_USE_UNICODE_INTERNALS 0
  #undef CYTHON_USE_UNICODE_WRITER
  #define CYTHON_USE_UNICODE_WRITER 0
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #undef CYTHON_AVOID_BORROWED_REFS
  #define CYTHON_AVOID_BORROWED_REFS 1
  #undef CYTHON_ASSUME_SAFE_MACROS
  #define CYTHON_ASSUME_SAFE_MACROS 0
  #undef CYTHON_UNPACK_METHODS
  #define CYTHON_UNPACK_METHODS 0
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_GIL
  #define CYTHON_FAST_GIL 0
  #undef CYTHON_METH_FASTCALL
  #define CYTHON_METH_FASTCALL 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #ifndef CYTHON_PEP487_INIT_SUBCLASS
    #define CYTHON_PEP487_INIT_SUBCLASS (PY_MAJOR_VERSION >= 3)
  #endif
  #undef CYTHON_PEP489_MULTI_PHASE_INIT
  #define CYTHON_PEP489_MULTI_PHASE_INIT 1
  #undef CYTHON_USE_MODULE_STATE
  #define CYTHON_USE_MODULE_STATE 0
  #undef CYTHON_USE_TP_FINALIZE
  #define CYTHON_USE_TP_FINALIZE 0
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC 0
  #endif
#elif defined(PYPY_VERSION)
  #define CYTHON_COMPILING_IN_PYPY 1
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_LIMITED_API 0
  #define CYTHON_COMPILING_IN_GRAAL 0
  #define CYTHON_COMPILING_IN_NOGIL 0
  #undef CYTHON_USE_TYPE_SLOTS
  #define CYTHON_USE_TYPE_SLOTS 0
  #ifndef CYTHON_USE_TYPE_SPECS
    #define CYTHON_USE_TYPE_SPECS 0
  #endif
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #if PY_VERSION_HEX < 0x03050000
    #undef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 0
  #elif !defined(CYTHON_USE_ASYNC_SLOTS)
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #undef CYTHON_USE_UNICODE_INTERNALS
  #define CYTHON_USE_UNICODE_INTERNALS 0
  #undef CYTHON_USE_UNICODE_WRITER
  #define CYTHON_USE_UNICODE_WRITER 0
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #undef CYTHON_AVOID_BORROWED_REFS
  #define CYTHON_AVOID_BORROWED_REFS 1
  #undef CYTHON_ASSUME_SAFE_MACROS
  #define CYTHON_ASSUME_SAFE_MACROS 0
  #undef CYTHON_UNPACK_METHODS
  #define CYTHON_UNPACK_METHODS 0
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_GIL
  #define CYTHON_FAST_GIL 0
  #undef CYTHON_METH_FASTCALL
  #define CYTHON_METH_FASTCALL 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #ifndef CYTHON_PEP487_INIT_SUBCLASS
    #define CYTHON_PEP487_INIT_SUBCLASS (PY_MAJOR_VERSION >= 3)
  #endif
  #if PY_VERSION_HEX < 0x03090000
    #undef CYTHON_PEP489_MULTI_PHASE_INIT
    #define CYTHON_PEP489_MULTI_PHASE_INIT 0
  #elif !defined(CYTHON_PEP489_MULTI_PHASE_INIT)
    #define CYTHON_PEP489_MULTI_PHASE_INIT 1
  #endif
  #undef CYTHON_USE_MODULE_STATE
  #define CYTHON_USE_MODULE_STATE 0
  #undef CYTHON_USE_TP_FINALIZE
  #define CYTHON_USE_TP_FINALIZE (PY_VERSION_HEX >= 0x030400a1 && PYPY_VERSION_NUM >= 0x07030C00)
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC 0
  #endif
#elif defined(CYTHON_LIMITED_API)
  #ifdef Py_LIMITED_API
    #undef __PYX_LIMITED_VERSION_HEX
    #define __PYX_LIMITED_VERSION_HEX Py_LIMITED_API
  #endif
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_LIMITED_API 1
  #define CYTHON_COMPILING_IN_GRAAL 0
  #define CYTHON_COMPILING_IN_NOGIL 0
  #undef CYTHON_CLINE_IN_TRACEBACK
  #define CYTHON_CLINE_IN_TRACEBACK 0
  #undef CYTHON_USE_TYPE_SLOTS
  #define CYTHON_USE_TYPE_SLOTS 0
  #undef CYTHON_USE_TYPE_SPECS
  #define CYTHON_USE_TYPE_SPECS 1
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #undef CYTHON_USE_ASYNC_SLOTS
  #define CYTHON_USE_ASYNC_SLOTS 0
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #undef CYTHON_USE_UNICODE_INTERNALS
  #define CYTHON_USE_UNICODE_INTERNALS 0
  #ifndef CYTHON_USE_UNICODE_WRITER
    #define CYTHON_USE_UNICODE_WRITER 0
  #endif
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #ifndef CYTHON_AVOID_BORROWED_REFS
    #define CYTHON_AVOID_BORROWED_REFS 0
  #endif
  #undef CYTHON_ASSUME_SAFE_MACROS
  #define CYTHON_ASSUME_SAFE_MACROS 0
  #undef CYTHON_UNPACK_METHODS
  #define CYTHON_UNPACK_METHODS 0
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_GIL
  #define CYTHON_FAST_GIL 0
  #undef CYTHON_METH_FASTCALL
  #define CYTHON_METH_FASTCALL 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #ifndef CYTHON_PEP487_INIT_SUBCLASS
    #define CYTHON_PEP487_INIT_SUBCLASS 1
  #endif
  #undef CYTHON_PEP489_MULTI_PHASE_INIT
  #define CYTHON_PEP489_MULTI_PHASE_INIT 0
  #undef CYTHON_USE_MODULE_STATE
  #define CYTHON_USE_MODULE_STATE 1
  #ifndef CYTHON_USE_TP_FINALIZE
    #define CYTHON_USE_TP_FINALIZE 0
  #endif
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC 0
  #endif
#elif defined(Py_GIL_DISABLED) || defined(Py_NOGIL)
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_LIMITED_API 0
  #define CYTHON_COMPILING_IN_GRAAL 0
  #define CYTHON_COMPILING_IN_NOGIL 1
  #ifndef CYTHON_USE_TYPE_SLOTS
    #define CYTHON_USE_TYPE_SLOTS 1
  #endif
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #ifndef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #ifndef CYTHON_USE_UNICODE_INTERNALS
    #define CYTHON_USE_UNICODE_INTERNALS 1
  #endif
  #undef CYTHON_USE_UNICODE_WRITER
  #define CYTHON_USE_UNICODE_WRITER 0
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #ifndef CYTHON_AVOID_BORROWED_REFS
    #define CYTHON_AVOID_BORROWED_REFS 0
  #endif
  #ifndef CYTHON_ASSUME_SAFE_MACROS
    #define CYTHON_ASSUME_SAFE_MACROS 1
  #endif
  #ifndef CYTHON_UNPACK_METHODS
    #define CYTHON_UNPACK_METHODS 1
  #endif
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #ifndef CYTHON_PEP489_MULTI_PHASE_INIT
    #define CYTHON_PEP489_MULTI_PHASE_INIT 1
  #endif
  #ifndef CYTHON_USE_TP_FINALIZE
    #define CYTHON_USE_TP_FINALIZE 1
  #endif
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
#else
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_CPYTHON 1
  #define CYTHON_COMPILING_IN_LIMITED_API 0
  #define CYTHON_COMPILING_IN_GRAAL 0
  #define CYTHON_COMPILING_IN_NOGIL 0
  #ifndef CYTHON_USE_TYPE_SLOTS
    #define CYTHON_USE_TYPE_SLOTS 1
  #endif
  #ifndef CYTHON_USE_TYPE_SPECS
    #define CYTHON_USE_TYPE_SPECS 0
  #endif
  #ifndef CYTHON_USE_PYTYPE_LOOKUP
    #define CYTHON_USE_PYTYPE_LOOKUP 1
  #endif
  #if PY_MAJOR_VERSION < 3
    #undef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 0
  #elif !defined(CYTHON_USE_ASYNC_SLOTS)
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #ifndef CYTHON_USE_PYLONG_INTERNALS
    #define CYTHON_USE_PYLONG_INTERNALS 1
  #endif
  #ifndef CYTHON_USE_PYLIST_INTERNALS
    #define CYTHON_USE_PYLIST_INTERNALS 1
  #endif
  #ifndef CYTHON_USE_UNICODE_INTERNALS
    #define CYTHON_USE_UNICODE_INTERNALS 1
  #endif
  #if PY_VERSION_HEX < 0x030300F0 || PY_VERSION_HEX >= 0x030B00A2
    #undef CYTHON_USE_UNICODE_WRITER
    #define CYTHON_USE_UNICODE_WRITER 0
  #elif !defined(CYTHON_USE_UNICODE_WRITER)
    #define CYTHON_USE_UNICODE_WRITER 1
  #endif
  #ifndef CYTHON_AVOID_BORROWED_REFS
    #define CYTHON_AVOID_BORROWED_REFS 0
  #endif
  #ifndef CYTHON_ASSUME_SAFE_MACROS
    #define CYTHON_ASSUME_SAFE_MACROS 1
  #endif
  #ifndef CYTHON_UNPACK_METHODS
    #define CYTHON_UNPACK_METHODS 1
  #endif
  #ifndef CYTHON_FAST_THREAD_STATE
    #define CYTHON_FAST_THREAD_STATE 1
  #endif
  #ifndef CYTHON_FAST_GIL
    #define CYTHON_FAST_GIL (PY_MAJOR_VERSION < 3 || PY_VERSION_HEX >= 0x03060000 && PY_VERSION_HEX < 0x030C00A6)
  #endif
  #ifndef CYTHON_METH_FASTCALL
    #define CYTHON_METH_FASTCALL (PY_VERSION_HEX >= 0x030700A1)
  #endif
  #ifndef CYTHON_FAST_PYCALL
    #define CYTHON_FAST_PYCALL 1
  #endif
  #ifndef CYTHON_PEP487_INIT_SUBCLASS
    #define CYTHON_PEP487_INIT_SUBCLASS 1
  #endif
  #if PY_VERSION_HEX < 0x03050000
    #undef CYTHON_PEP489_MULTI_PHASE_INIT
    #define CYTHON_PEP489_MULTI_PHASE_INIT 0
  #elif !defined(CYTHON_PEP489_MULTI_PHASE_INIT)
    #define CYTHON_PEP489_MULTI_PHASE_INIT 1
  #endif
  #ifndef CYTHON_USE_MODULE_STATE
    #define CYTHON_USE_MODULE_STATE 0
  #endif
  #if PY_VERSION_HEX < 0x030400a1
    #undef CYTHON_USE_TP_FINALIZE
    #define CYTHON_USE_TP_FINALIZE 0
  #elif !defined(CYTHON_USE_TP_FINALIZE)
    #define CYTHON_USE_TP_FINALIZE 1
  #endif
  #if PY_VERSION_HEX < 0x030600B1
    #undef CYTHON_USE_DICT_VERSIONS
    #define CYTHON_USE_DICT_VERSIONS 0
  #elif !defined(CYTHON_USE_DICT_VERSIONS)
    #define CYTHON_USE_DICT_VERSIONS  (PY_VERSION_HEX < 0x030C00A5)
  #endif
  #if PY_VERSION_HEX < 0x030700A3
    #undef CYTHON_USE_EXC_INFO_STACK
    #define CYTHON_USE_EXC_INFO_STACK 0
  #elif !defined(CYTHON_USE_EXC_INFO_STACK)
    #define CYTHON_USE_EXC_INFO_STACK 1
  #endif
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC 1
  #endif
#endif
#if !defined(CYTHON_FAST_PYCCALL)
#define CYTHON_FAST_PYCCALL  (CYTHON_FAST_PYCALL && PY_VERSION_HEX >= 0x030600B1)
#endif
#if !defined(CYTHON_VECTORCALL)
#define CYTHON_VECTORCALL  (CYTHON_FAST_PYCCALL && PY_VERSION_HEX >= 0x030800B1)
#endif
#define CYTHON_BACKPORT_VECTORCALL (CYTHON_METH_FASTCALL && PY_VERSION_HEX < 0x030800B1)
#if CYTHON_USE_PYLONG_INTERNALS
  #if PY_MAJOR_VERSION < 3
    #include "longintrepr.h"
  #endif
  #undef SHIFT
  #undef BASE
  #undef MASK
  #ifdef SIZEOF_VOID_P
    enum { __pyx_check_sizeof_voidp = 1 / (int)(SIZEOF_VOID_P == sizeof(void*)) };
  #endif
#endif
#ifndef __has_attribute
  #define __has_attribute(x) 0
#endif
#ifndef __has_cpp_attribute
  #define __has_cpp_attribute(x) 0
#endif
#ifndef CYTHON_RESTRICT
  #if defined(__GNUC__)
    #define CYTHON_RESTRICT __restrict__
  #elif defined(_MSC_VER) && _MSC_VER >= 1400
    #define CYTHON_RESTRICT __restrict
  #elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define CYTHON_RESTRICT restrict
  #else
    #define CYTHON_RESTRICT
  #endif
#endif
#ifndef CYTHON_UNUSED
  #if defined(__cplusplus)
    
    #if ((defined(_MSVC_LANG) && _MSVC_LANG >= 201703L) || __cplusplus >= 201703L)
      #if __has_cpp_attribute(maybe_unused)
        #define CYTHON_UNUSED [[maybe_unused]]
      #endif
    #endif
  #endif
#endif
#ifndef CYTHON_UNUSED
# if defined(__GNUC__)
#   if !(defined(__cplusplus)) || (__GNUC__ > 3 || (__GNUC__ == 3 && __GNUC_MINOR__ >= 4))
#     define CYTHON_UNUSED __attribute__ ((__unused__))
#   else
#     define CYTHON_UNUSED
#   endif
# elif defined(__ICC) || (defined(__INTEL_COMPILER) && !defined(_MSC_VER))
#   define CYTHON_UNUSED __attribute__ ((__unused__))
# else
#   define CYTHON_UNUSED
# endif
#endif
#ifndef CYTHON_UNUSED_VAR
#  if defined(__cplusplus)
     template<class T> void CYTHON_UNUSED_VAR( const T& ) { }
#  else
#    define CYTHON_UNUSED_VAR(x) (void)(x)
#  endif
#endif
#ifndef CYTHON_MAYBE_UNUSED_VAR
  #define CYTHON_MAYBE_UNUSED_VAR(x) CYTHON_UNUSED_VAR(x)
#endif
#ifndef CYTHON_NCP_UNUSED
# if CYTHON_COMPILING_IN_CPYTHON
#  define CYTHON_NCP_UNUSED
# else
#  define CYTHON_NCP_UNUSED CYTHON_UNUSED
# endif
#endif
#ifndef CYTHON_USE_CPP_STD_MOVE
  #if defined(__cplusplus) && (\
    __cplusplus >= 201103L || (defined(_MSC_VER) && _MSC_VER >= 1600))
    #define CYTHON_USE_CPP_STD_MOVE 1
  #else
    #define CYTHON_USE_CPP_STD_MOVE 0
  #endif
#endif
#define __Pyx_void_to_None(void_result) ((void)(void_result), Py_INCREF(Py_None), Py_None)
#ifdef _MSC_VER
    #ifndef _MSC_STDINT_H_
        #if _MSC_VER < 1300
            typedef unsigned char     uint8_t;
            typedef unsigned short    uint16_t;
            typedef unsigned int      uint32_t;
        #else
            typedef unsigned __int8   uint8_t;
            typedef unsigned __int16  uint16_t;
            typedef unsigned __int32  uint32_t;
        #endif
    #endif
    #if _MSC_VER < 1300
        #ifdef _WIN64
            typedef unsigned long long  __pyx_uintptr_t;
        #else
            typedef unsigned int        __pyx_uintptr_t;
        #endif
    #else
        #ifdef _WIN64
            typedef unsigned __int64    __pyx_uintptr_t;
        #else
            typedef unsigned __int32    __pyx_uintptr_t;
        #endif
    #endif
#else
    #include <stdint.h>
    typedef uintptr_t  __pyx_uintptr_t;
#endif
#ifndef CYTHON_FALLTHROUGH
  #if defined(__cplusplus)
    
    #if ((defined(_MSVC_LANG) && _MSVC_LANG >= 201703L) || __cplusplus >= 201703L)
      #if __has_cpp_attribute(fallthrough)
        #define CYTHON_FALLTHROUGH [[fallthrough]]
      #endif
    #endif
    #ifndef CYTHON_FALLTHROUGH
      #if __has_cpp_attribute(clang::fallthrough)
        #define CYTHON_FALLTHROUGH [[clang::fallthrough]]
      #elif __has_cpp_attribute(gnu::fallthrough)
        #define CYTHON_FALLTHROUGH [[gnu::fallthrough]]
      #endif
    #endif
  #endif
  #ifndef CYTHON_FALLTHROUGH
    #if __has_attribute(fallthrough)
      #define CYTHON_FALLTHROUGH __attribute__((fallthrough))
    #else
      #define CYTHON_FALLTHROUGH
    #endif
  #endif
  #if defined(__clang__) && defined(__apple_build_version__)
    #if __apple_build_version__ < 7000000
      #undef  CYTHON_FALLTHROUGH
      #define CYTHON_FALLTHROUGH
    #endif
  #endif
#endif
#ifdef __cplusplus
  template <typename T>
  struct __PYX_IS_UNSIGNED_IMPL {static const bool value = T(0) < T(-1);};
  #define __PYX_IS_UNSIGNED(type) (__PYX_IS_UNSIGNED_IMPL<type>::value)
#else
  #define __PYX_IS_UNSIGNED(type) (((type)-1) > 0)
#endif
#if CYTHON_COMPILING_IN_PYPY == 1
  #define __PYX_NEED_TP_PRINT_SLOT  (PY_VERSION_HEX >= 0x030800b4 && PY_VERSION_HEX < 0x030A0000)
#else
  #define __PYX_NEED_TP_PRINT_SLOT  (PY_VERSION_HEX >= 0x030800b4 && PY_VERSION_HEX < 0x03090000)
#endif
#define __PYX_REINTERPRET_FUNCION(func_pointer, other_pointer) ((func_pointer)(void(*)(void))(other_pointer))

#ifndef CYTHON_INLINE
  #if defined(__clang__)
    #define CYTHON_INLINE __inline__ __attribute__ ((__unused__))
  #elif defined(__GNUC__)
    #define CYTHON_INLINE __inline__
  #elif defined(_MSC_VER)
    #define CYTHON_INLINE __inline
  #elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define CYTHON_INLINE inline
  #else
    #define CYTHON_INLINE
  #endif
#endif

#define __PYX_BUILD_PY_SSIZE_T "n"
#define CYTHON_FORMAT_SSIZE_T "z"
#if PY_MAJOR_VERSION < 3
  #define __Pyx_BUILTIN_MODULE_NAME "__builtin__"
  #define __Pyx_DefaultClassType PyClass_Type
  #define __Pyx_PyCode_New(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_New(a+k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
#else
  #define __Pyx_BUILTIN_MODULE_NAME "builtins"
  #define __Pyx_DefaultClassType PyType_Type
#if CYTHON_COMPILING_IN_LIMITED_API
    static CYTHON_INLINE PyObject* __Pyx_PyCode_New(int a, int p, int k, int l, int s, int f,
                                                    PyObject *code, PyObject *c, PyObject* n, PyObject *v,
                                                    PyObject *fv, PyObject *cell, PyObject* fn,
                                                    PyObject *name, int fline, PyObject *lnos) {
        PyObject *exception_table = NULL;
        PyObject *types_module=NULL, *code_type=NULL, *result=NULL;
        #if __PYX_LIMITED_VERSION_HEX < 0x030B0000
        PyObject *version_info; // borrowed
        PyObject *py_minor_version = NULL;
        #endif
        long minor_version = 0;
        PyObject *type, *value, *traceback;
        PyErr_Fetch(&type, &value, &traceback);
        #if __PYX_LIMITED_VERSION_HEX >= 0x030B0000
        minor_version = 11; // we don't yet need to distinguish between versions > 11
        #else
        if (!(version_info = PySys_GetObject("version_info"))) goto end;
        if (!(py_minor_version = PySequence_GetItem(version_info, 1))) goto end;
        minor_version = PyLong_AsLong(py_minor_version);
        Py_DECREF(py_minor_version);
        if (minor_version == -1 && PyErr_Occurred()) goto end;
        #endif
        if (!(types_module = PyImport_ImportModule("types"))) goto end;
        if (!(code_type = PyObject_GetAttrString(types_module, "CodeType"))) goto end;
        if (minor_version <= 7) {
            (void)p;
            result = PyObject_CallFunction(code_type, "iiiiiOOOOOOiOO", a, k, l, s, f, code,
                          c, n, v, fn, name, fline, lnos, fv, cell);
        } else if (minor_version <= 10) {
            result = PyObject_CallFunction(code_type, "iiiiiiOOOOOOiOO", a,p, k, l, s, f, code,
                          c, n, v, fn, name, fline, lnos, fv, cell);
        } else {
            if (!(exception_table = PyBytes_FromStringAndSize(NULL, 0))) goto end;
            result = PyObject_CallFunction(code_type, "iiiiiiOOOOOOOiOO", a,p, k, l, s, f, code,
                          c, n, v, fn, name, name, fline, lnos, exception_table, fv, cell);
        }
    end:
        Py_XDECREF(code_type);
        Py_XDECREF(exception_table);
        Py_XDECREF(types_module);
        if (type) {
            PyErr_Restore(type, value, traceback);
        }
        return result;
    }
    #ifndef CO_OPTIMIZED
    #define CO_OPTIMIZED 0x0001
    #endif
    #ifndef CO_NEWLOCALS
    #define CO_NEWLOCALS 0x0002
    #endif
    #ifndef CO_VARARGS
    #define CO_VARARGS 0x0004
    #endif
    #ifndef CO_VARKEYWORDS
    #define CO_VARKEYWORDS 0x0008
    #endif
    #ifndef CO_ASYNC_GENERATOR
    #define CO_ASYNC_GENERATOR 0x0200
    #endif
    #ifndef CO_GENERATOR
    #define CO_GENERATOR 0x0020
    #endif
    #ifndef CO_COROUTINE
    #define CO_COROUTINE 0x0080
    #endif
#elif PY_VERSION_HEX >= 0x030B0000
  static CYTHON_INLINE PyCodeObject* __Pyx_PyCode_New(int a, int p, int k, int l, int s, int f,
                                                    PyObject *code, PyObject *c, PyObject* n, PyObject *v,
                                                    PyObject *fv, PyObject *cell, PyObject* fn,
                                                    PyObject *name, int fline, PyObject *lnos) {
    PyCodeObject *result;
    PyObject *empty_bytes = PyBytes_FromStringAndSize("", 0);  // we don't have access to __pyx_empty_bytes here
    if (!empty_bytes) return NULL;
    result =
      #if PY_VERSION_HEX >= 0x030C0000
        PyUnstable_Code_NewWithPosOnlyArgs
      #else
        PyCode_NewWithPosOnlyArgs
      #endif
        (a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, name, fline, lnos, empty_bytes);
    Py_DECREF(empty_bytes);
    return result;
  }
#elif PY_VERSION_HEX >= 0x030800B2 && !CYTHON_COMPILING_IN_PYPY
  #define __Pyx_PyCode_New(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_NewWithPosOnlyArgs(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
#else
  #define __Pyx_PyCode_New(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_New(a, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
#endif
#endif
#if PY_VERSION_HEX >= 0x030900A4 || defined(Py_IS_TYPE)
  #define __Pyx_IS_TYPE(ob, type) Py_IS_TYPE(ob, type)
#else
  #define __Pyx_IS_TYPE(ob, type) (((const PyObject*)ob)->ob_type == (type))
#endif
#if PY_VERSION_HEX >= 0x030A00B1 || defined(Py_Is)
  #define __Pyx_Py_Is(x, y)  Py_Is(x, y)
#else
  #define __Pyx_Py_Is(x, y) ((x) == (y))
#endif
#if PY_VERSION_HEX >= 0x030A00B1 || defined(Py_IsNone)
  #define __Pyx_Py_IsNone(ob) Py_IsNone(ob)
#else
  #define __Pyx_Py_IsNone(ob) __Pyx_Py_Is((ob), Py_None)
#endif
#if PY_VERSION_HEX >= 0x030A00B1 || defined(Py_IsTrue)
  #define __Pyx_Py_IsTrue(ob) Py_IsTrue(ob)
#else
  #define __Pyx_Py_IsTrue(ob) __Pyx_Py_Is((ob), Py_True)
#endif
#if PY_VERSION_HEX >= 0x030A00B1 || defined(Py_IsFalse)
  #define __Pyx_Py_IsFalse(ob) Py_IsFalse(ob)
#else
  #define __Pyx_Py_IsFalse(ob) __Pyx_Py_Is((ob), Py_False)
#endif
#define __Pyx_NoneAsNull(obj)  (__Pyx_Py_IsNone(obj) ? NULL : (obj))
#if PY_VERSION_HEX >= 0x030900F0 && !CYTHON_COMPILING_IN_PYPY
  #define __Pyx_PyObject_GC_IsFinalized(o) PyObject_GC_IsFinalized(o)
#else
  #define __Pyx_PyObject_GC_IsFinalized(o) _PyGC_FINALIZED(o)
#endif
#ifndef CO_COROUTINE
  #define CO_COROUTINE 0x80
#endif
#ifndef CO_ASYNC_GENERATOR
  #define CO_ASYNC_GENERATOR 0x200
#endif
#ifndef Py_TPFLAGS_CHECKTYPES
  #define Py_TPFLAGS_CHECKTYPES 0
#endif
#ifndef Py_TPFLAGS_HAVE_INDEX
  #define Py_TPFLAGS_HAVE_INDEX 0
#endif
#ifndef Py_TPFLAGS_HAVE_NEWBUFFER
  #define Py_TPFLAGS_HAVE_NEWBUFFER 0
#endif
#ifndef Py_TPFLAGS_HAVE_FINALIZE
  #define Py_TPFLAGS_HAVE_FINALIZE 0
#endif
#ifndef Py_TPFLAGS_SEQUENCE
  #define Py_TPFLAGS_SEQUENCE 0
#endif
#ifndef Py_TPFLAGS_MAPPING
  #define Py_TPFLAGS_MAPPING 0
#endif
#ifndef METH_STACKLESS
  #define METH_STACKLESS 0
#endif
#if PY_VERSION_HEX <= 0x030700A3 || !defined(METH_FASTCALL)
  #ifndef METH_FASTCALL
     #define METH_FASTCALL 0x80
  #endif
  typedef PyObject *(*__Pyx_PyCFunctionFast) (PyObject *self, PyObject *const *args, Py_ssize_t nargs);
  typedef PyObject *(*__Pyx_PyCFunctionFastWithKeywords) (PyObject *self, PyObject *const *args,
                                                          Py_ssize_t nargs, PyObject *kwnames);
#else
  #define __Pyx_PyCFunctionFast _PyCFunctionFast
  #define __Pyx_PyCFunctionFastWithKeywords _PyCFunctionFastWithKeywords
#endif
#if CYTHON_METH_FASTCALL
  #define __Pyx_METH_FASTCALL METH_FASTCALL
  #define __Pyx_PyCFunction_FastCall __Pyx_PyCFunctionFast
  #define __Pyx_PyCFunction_FastCallWithKeywords __Pyx_PyCFunctionFastWithKeywords
#else
  #define __Pyx_METH_FASTCALL METH_VARARGS
  #define __Pyx_PyCFunction_FastCall PyCFunction
  #define __Pyx_PyCFunction_FastCallWithKeywords PyCFunctionWithKeywords
#endif
#if CYTHON_VECTORCALL
  #define __pyx_vectorcallfunc vectorcallfunc
  #define __Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET  PY_VECTORCALL_ARGUMENTS_OFFSET
  #define __Pyx_PyVectorcall_NARGS(n)  PyVectorcall_NARGS((size_t)(n))
#elif CYTHON_BACKPORT_VECTORCALL
  typedef PyObject *(*__pyx_vectorcallfunc)(PyObject *callable, PyObject *const *args,
                                            size_t nargsf, PyObject *kwnames);
  #define __Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET  ((size_t)1 << (8 * sizeof(size_t) - 1))
  #define __Pyx_PyVectorcall_NARGS(n)  ((Py_ssize_t)(((size_t)(n)) & ~__Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET))
#else
  #define __Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET  0
  #define __Pyx_PyVectorcall_NARGS(n)  ((Py_ssize_t)(n))
#endif
#if PY_MAJOR_VERSION >= 0x030900B1
#define __Pyx_PyCFunction_CheckExact(func)  PyCFunction_CheckExact(func)
#else
#define __Pyx_PyCFunction_CheckExact(func)  PyCFunction_Check(func)
#endif
#define __Pyx_CyOrPyCFunction_Check(func)  PyCFunction_Check(func)
#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_CyOrPyCFunction_GET_FUNCTION(func)  (((PyCFunctionObject*)(func))->m_ml->ml_meth)
#elif !CYTHON_COMPILING_IN_LIMITED_API
#define __Pyx_CyOrPyCFunction_GET_FUNCTION(func)  PyCFunction_GET_FUNCTION(func)
#endif
#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_CyOrPyCFunction_GET_FLAGS(func)  (((PyCFunctionObject*)(func))->m_ml->ml_flags)
static CYTHON_INLINE PyObject* __Pyx_CyOrPyCFunction_GET_SELF(PyObject *func) {
    return (__Pyx_CyOrPyCFunction_GET_FLAGS(func) & METH_STATIC) ? NULL : ((PyCFunctionObject*)func)->m_self;
}
#endif
static CYTHON_INLINE int __Pyx__IsSameCFunction(PyObject *func, void *cfunc) {
#if CYTHON_COMPILING_IN_LIMITED_API
    return PyCFunction_Check(func) && PyCFunction_GetFunction(func) == (PyCFunction) cfunc;
#else
    return PyCFunction_Check(func) && PyCFunction_GET_FUNCTION(func) == (PyCFunction) cfunc;
#endif
}
#define __Pyx_IsSameCFunction(func, cfunc)   __Pyx__IsSameCFunction(func, cfunc)
#if __PYX_LIMITED_VERSION_HEX < 0x030900B1
  #define __Pyx_PyType_FromModuleAndSpec(m, s, b)  ((void)m, PyType_FromSpecWithBases(s, b))
  typedef PyObject *(*__Pyx_PyCMethod)(PyObject *, PyTypeObject *, PyObject *const *, size_t, PyObject *);
#else
  #define __Pyx_PyType_FromModuleAndSpec(m, s, b)  PyType_FromModuleAndSpec(m, s, b)
  #define __Pyx_PyCMethod  PyCMethod
#endif
#ifndef METH_METHOD
  #define METH_METHOD 0x200
#endif
#if CYTHON_COMPILING_IN_PYPY && !defined(PyObject_Malloc)
  #define PyObject_Malloc(s)   PyMem_Malloc(s)
  #define PyObject_Free(p)     PyMem_Free(p)
  #define PyObject_Realloc(p)  PyMem_Realloc(p)
#endif
#if CYTHON_COMPILING_IN_LIMITED_API
  #define __Pyx_PyCode_HasFreeVars(co)  (PyCode_GetNumFree(co) > 0)
  #define __Pyx_PyFrame_SetLineNumber(frame, lineno)
#else
  #define __Pyx_PyCode_HasFreeVars(co)  (PyCode_GetNumFree(co) > 0)
  #define __Pyx_PyFrame_SetLineNumber(frame, lineno)  (frame)->f_lineno = (lineno)
#endif
#if CYTHON_COMPILING_IN_LIMITED_API
  #define __Pyx_PyThreadState_Current PyThreadState_Get()
#elif !CYTHON_FAST_THREAD_STATE
  #define __Pyx_PyThreadState_Current PyThreadState_GET()
#elif PY_VERSION_HEX >= 0x030d00A1
  #define __Pyx_PyThreadState_Current PyThreadState_GetUnchecked()
#elif PY_VERSION_HEX >= 0x03060000
  #define __Pyx_PyThreadState_Current _PyThreadState_UncheckedGet()
#elif PY_VERSION_HEX >= 0x03000000
  #define __Pyx_PyThreadState_Current PyThreadState_GET()
#else
  #define __Pyx_PyThreadState_Current _PyThreadState_Current
#endif
#if CYTHON_COMPILING_IN_LIMITED_API
static CYTHON_INLINE void *__Pyx_PyModule_GetState(PyObject *op)
{
    void *result;
    result = PyModule_GetState(op);
    if (!result)
        Py_FatalError("Couldn't find the module state");
    return result;
}
#endif
#define __Pyx_PyObject_GetSlot(obj, name, func_ctype)  __Pyx_PyType_GetSlot(Py_TYPE(obj), name, func_ctype)
#if CYTHON_COMPILING_IN_LIMITED_API
  #define __Pyx_PyType_GetSlot(type, name, func_ctype)  ((func_ctype) PyType_GetSlot((type), Py_##name))
#else
  #define __Pyx_PyType_GetSlot(type, name, func_ctype)  ((type)->name)
#endif
#if PY_VERSION_HEX < 0x030700A2 && !defined(PyThread_tss_create) && !defined(Py_tss_NEEDS_INIT)
#include "pythread.h"
#define Py_tss_NEEDS_INIT 0
typedef int Py_tss_t;
static CYTHON_INLINE int PyThread_tss_create(Py_tss_t *key) {
  *key = PyThread_create_key();
  return 0;
}
static CYTHON_INLINE Py_tss_t * PyThread_tss_alloc(void) {
  Py_tss_t *key = (Py_tss_t *)PyObject_Malloc(sizeof(Py_tss_t));
  *key = Py_tss_NEEDS_INIT;
  return key;
}
static CYTHON_INLINE void PyThread_tss_free(Py_tss_t *key) {
  PyObject_Free(key);
}
static CYTHON_INLINE int PyThread_tss_is_created(Py_tss_t *key) {
  return *key != Py_tss_NEEDS_INIT;
}
static CYTHON_INLINE void PyThread_tss_delete(Py_tss_t *key) {
  PyThread_delete_key(*key);
  *key = Py_tss_NEEDS_INIT;
}
static CYTHON_INLINE int PyThread_tss_set(Py_tss_t *key, void *value) {
  return PyThread_set_key_value(*key, value);
}
static CYTHON_INLINE void * PyThread_tss_get(Py_tss_t *key) {
  return PyThread_get_key_value(*key);
}
#endif
#if PY_MAJOR_VERSION < 3
    #if CYTHON_COMPILING_IN_PYPY
        #if PYPY_VERSION_NUM < 0x07030600
            #if defined(__cplusplus) && __cplusplus >= 201402L
                [[deprecated("`with nogil:` inside a nogil function will not release the GIL in PyPy2 < 7.3.6")]]
            #elif defined(__GNUC__) || defined(__clang__)
                __attribute__ ((__deprecated__("`with nogil:` inside a nogil function will not release the GIL in PyPy2 < 7.3.6")))
            #elif defined(_MSC_VER)
                __declspec(deprecated("`with nogil:` inside a nogil function will not release the GIL in PyPy2 < 7.3.6"))
            #endif
            static CYTHON_INLINE int PyGILState_Check(void) {
                return 0;
            }
        #else  // PYPY_VERSION_NUM < 0x07030600
        #endif  // PYPY_VERSION_NUM < 0x07030600
    #else
        static CYTHON_INLINE int PyGILState_Check(void) {
            PyThreadState * tstate = _PyThreadState_Current;
            return tstate && (tstate == PyGILState_GetThisThreadState());
        }
    #endif
#endif
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030d0000 || defined(_PyDict_NewPresized)
#define __Pyx_PyDict_NewPresized(n)  ((n <= 8) ? PyDict_New() : _PyDict_NewPresized(n))
#else
#define __Pyx_PyDict_NewPresized(n)  PyDict_New()
#endif
#if PY_MAJOR_VERSION >= 3 || CYTHON_FUTURE_DIVISION
  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_TrueDivide(x,y)
  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceTrueDivide(x,y)
#else
  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_Divide(x,y)
  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceDivide(x,y)
#endif
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX > 0x030600B4 && PY_VERSION_HEX < 0x030d0000 && CYTHON_USE_UNICODE_INTERNALS
#define __Pyx_PyDict_GetItemStrWithError(dict, name)  _PyDict_GetItem_KnownHash(dict, name, ((PyASCIIObject *) name)->hash)
static CYTHON_INLINE PyObject * __Pyx_PyDict_GetItemStr(PyObject *dict, PyObject *name) {
    PyObject *res = __Pyx_PyDict_GetItemStrWithError(dict, name);
    if (res == NULL) PyErr_Clear();
    return res;
}
#elif PY_MAJOR_VERSION >= 3 && (!CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM >= 0x07020000)
#define __Pyx_PyDict_GetItemStrWithError  PyDict_GetItemWithError
#define __Pyx_PyDict_GetItemStr           PyDict_GetItem
#else
static CYTHON_INLINE PyObject * __Pyx_PyDict_GetItemStrWithError(PyObject *dict, PyObject *name) {
#if CYTHON_COMPILING_IN_PYPY
    return PyDict_GetItem(dict, name);
#else
    PyDictEntry *ep;
    PyDictObject *mp = (PyDictObject*) dict;
    long hash = ((PyStringObject *) name)->ob_shash;
    assert(hash != -1);
    ep = (mp->ma_lookup)(mp, name, hash);
    if (ep == NULL) {
        return NULL;
    }
    return ep->me_value;
#endif
}
#define __Pyx_PyDict_GetItemStr           PyDict_GetItem
#endif
#if CYTHON_USE_TYPE_SLOTS
  #define __Pyx_PyType_GetFlags(tp)   (((PyTypeObject *)tp)->tp_flags)
  #define __Pyx_PyType_HasFeature(type, feature)  ((__Pyx_PyType_GetFlags(type) & (feature)) != 0)
  #define __Pyx_PyObject_GetIterNextFunc(obj)  (Py_TYPE(obj)->tp_iternext)
#else
  #define __Pyx_PyType_GetFlags(tp)   (PyType_GetFlags((PyTypeObject *)tp))
  #define __Pyx_PyType_HasFeature(type, feature)  PyType_HasFeature(type, feature)
  #define __Pyx_PyObject_GetIterNextFunc(obj)  PyIter_Next
#endif
#if CYTHON_COMPILING_IN_LIMITED_API
  #define __Pyx_SetItemOnTypeDict(tp, k, v) PyObject_GenericSetAttr((PyObject*)tp, k, v)
#else
  #define __Pyx_SetItemOnTypeDict(tp, k, v) PyDict_SetItem(tp->tp_dict, k, v)
#endif
#if CYTHON_USE_TYPE_SPECS && PY_VERSION_HEX >= 0x03080000
#define __Pyx_PyHeapTypeObject_GC_Del(obj)  {\
    PyTypeObject *type = Py_TYPE((PyObject*)obj);\
    assert(__Pyx_PyType_HasFeature(type, Py_TPFLAGS_HEAPTYPE));\
    PyObject_GC_Del(obj);\
    Py_DECREF(type);\
}
#else
#define __Pyx_PyHeapTypeObject_GC_Del(obj)  PyObject_GC_Del(obj)
#endif
#if CYTHON_COMPILING_IN_LIMITED_API
  #define CYTHON_PEP393_ENABLED 1
  #define __Pyx_PyUnicode_READY(op)       (0)
  #define __Pyx_PyUnicode_GET_LENGTH(u)   PyUnicode_GetLength(u)
  #define __Pyx_PyUnicode_READ_CHAR(u, i) PyUnicode_ReadChar(u, i)
  #define __Pyx_PyUnicode_MAX_CHAR_VALUE(u)   ((void)u, 1114111U)
  #define __Pyx_PyUnicode_KIND(u)         ((void)u, (0))
  #define __Pyx_PyUnicode_DATA(u)         ((void*)u)
  #define __Pyx_PyUnicode_READ(k, d, i)   ((void)k, PyUnicode_ReadChar((PyObject*)(d), i))
  #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != PyUnicode_GetLength(u))
#elif PY_VERSION_HEX > 0x03030000 && defined(PyUnicode_KIND)
  #define CYTHON_PEP393_ENABLED 1
  #if PY_VERSION_HEX >= 0x030C0000
    #define __Pyx_PyUnicode_READY(op)       (0)
  #else
    #define __Pyx_PyUnicode_READY(op)       (likely(PyUnicode_IS_READY(op)) ?\
                                                0 : _PyUnicode_Ready((PyObject *)(op)))
  #endif
  #define __Pyx_PyUnicode_GET_LENGTH(u)   PyUnicode_GET_LENGTH(u)
  #define __Pyx_PyUnicode_READ_CHAR(u, i) PyUnicode_READ_CHAR(u, i)
  #define __Pyx_PyUnicode_MAX_CHAR_VALUE(u)   PyUnicode_MAX_CHAR_VALUE(u)
  #define __Pyx_PyUnicode_KIND(u)         ((int)PyUnicode_KIND(u))
  #define __Pyx_PyUnicode_DATA(u)         PyUnicode_DATA(u)
  #define __Pyx_PyUnicode_READ(k, d, i)   PyUnicode_READ(k, d, i)
  #define __Pyx_PyUnicode_WRITE(k, d, i, ch)  PyUnicode_WRITE(k, d, i, (Py_UCS4) ch)
  #if PY_VERSION_HEX >= 0x030C0000
    #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != PyUnicode_GET_LENGTH(u))
  #else
    #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x03090000
    #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != (likely(PyUnicode_IS_READY(u)) ? PyUnicode_GET_LENGTH(u) : ((PyCompactUnicodeObject *)(u))->wstr_length))
    #else
    #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != (likely(PyUnicode_IS_READY(u)) ? PyUnicode_GET_LENGTH(u) : PyUnicode_GET_SIZE(u)))
    #endif
  #endif
#else
  #define CYTHON_PEP393_ENABLED 0
  #define PyUnicode_1BYTE_KIND  1
  #define PyUnicode_2BYTE_KIND  2
  #define PyUnicode_4BYTE_KIND  4
  #define __Pyx_PyUnicode_READY(op)       (0)
  #define __Pyx_PyUnicode_GET_LENGTH(u)   PyUnicode_GET_SIZE(u)
  #define __Pyx_PyUnicode_READ_CHAR(u, i) ((Py_UCS4)(PyUnicode_AS_UNICODE(u)[i]))
  #define __Pyx_PyUnicode_MAX_CHAR_VALUE(u)   ((sizeof(Py_UNICODE) == 2) ? 65535U : 1114111U)
  #define __Pyx_PyUnicode_KIND(u)         ((int)sizeof(Py_UNICODE))
  #define __Pyx_PyUnicode_DATA(u)         ((void*)PyUnicode_AS_UNICODE(u))
  #define __Pyx_PyUnicode_READ(k, d, i)   ((void)(k), (Py_UCS4)(((Py_UNICODE*)d)[i]))
  #define __Pyx_PyUnicode_WRITE(k, d, i, ch)  (((void)(k)), ((Py_UNICODE*)d)[i] = (Py_UNICODE) ch)
  #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != PyUnicode_GET_SIZE(u))
#endif
#if CYTHON_COMPILING_IN_PYPY
  #define __Pyx_PyUnicode_Concat(a, b)      PyNumber_Add(a, b)
  #define __Pyx_PyUnicode_ConcatSafe(a, b)  PyNumber_Add(a, b)
#else
  #define __Pyx_PyUnicode_Concat(a, b)      PyUnicode_Concat(a, b)
  #define __Pyx_PyUnicode_ConcatSafe(a, b)  ((unlikely((a) == Py_None) || unlikely((b) == Py_None)) ?\
      PyNumber_Add(a, b) : __Pyx_PyUnicode_Concat(a, b))
#endif
#if CYTHON_COMPILING_IN_PYPY
  #if !defined(PyUnicode_DecodeUnicodeEscape)
    #define PyUnicode_DecodeUnicodeEscape(s, size, errors)  PyUnicode_Decode(s, size, "unicode_escape", errors)
  #endif
  #if !defined(PyUnicode_Contains) || (PY_MAJOR_VERSION == 2 && PYPY_VERSION_NUM < 0x07030500)
    #undef PyUnicode_Contains
    #define PyUnicode_Contains(u, s)  PySequence_Contains(u, s)
  #endif
  #if !defined(PyByteArray_Check)
    #define PyByteArray_Check(obj)  PyObject_TypeCheck(obj, &PyByteArray_Type)
  #endif
  #if !defined(PyObject_Format)
    #define PyObject_Format(obj, fmt)  PyObject_CallMethod(obj, "__format__", "O", fmt)
  #endif
#endif
#define __Pyx_PyString_FormatSafe(a, b)   ((unlikely((a) == Py_None || (PyString_Check(b) && !PyString_CheckExact(b)))) ? PyNumber_Remainder(a, b) : __Pyx_PyString_Format(a, b))
#define __Pyx_PyUnicode_FormatSafe(a, b)  ((unlikely((a) == Py_None || (PyUnicode_Check(b) && !PyUnicode_CheckExact(b)))) ? PyNumber_Remainder(a, b) : PyUnicode_Format(a, b))
#if PY_MAJOR_VERSION >= 3
  #define __Pyx_PyString_Format(a, b)  PyUnicode_Format(a, b)
#else
  #define __Pyx_PyString_Format(a, b)  PyString_Format(a, b)
#endif
#if PY_MAJOR_VERSION < 3 && !defined(PyObject_ASCII)
  #define PyObject_ASCII(o)            PyObject_Repr(o)
#endif
#if PY_MAJOR_VERSION >= 3
  #define PyBaseString_Type            PyUnicode_Type
  #define PyStringObject               PyUnicodeObject
  #define PyString_Type                PyUnicode_Type
  #define PyString_Check               PyUnicode_Check
  #define PyString_CheckExact          PyUnicode_CheckExact
#ifndef PyObject_Unicode
  #define PyObject_Unicode             PyObject_Str
#endif
#endif
#if PY_MAJOR_VERSION >= 3
  #define __Pyx_PyBaseString_Check(obj) PyUnicode_Check(obj)
  #define __Pyx_PyBaseString_CheckExact(obj) PyUnicode_CheckExact(obj)
#else
  #define __Pyx_PyBaseString_Check(obj) (PyString_Check(obj) || PyUnicode_Check(obj))
  #define __Pyx_PyBaseString_CheckExact(obj) (PyString_CheckExact(obj) || PyUnicode_CheckExact(obj))
#endif
#if CYTHON_COMPILING_IN_CPYTHON
  #define __Pyx_PySequence_ListKeepNew(obj)\
    (likely(PyList_CheckExact(obj) && Py_REFCNT(obj) == 1) ? __Pyx_NewRef(obj) : PySequence_List(obj))
#else
  #define __Pyx_PySequence_ListKeepNew(obj)  PySequence_List(obj)
#endif
#ifndef PySet_CheckExact
  #define PySet_CheckExact(obj)        __Pyx_IS_TYPE(obj, &PySet_Type)
#endif
#if PY_VERSION_HEX >= 0x030900A4
  #define __Pyx_SET_REFCNT(obj, refcnt) Py_SET_REFCNT(obj, refcnt)
  #define __Pyx_SET_SIZE(obj, size) Py_SET_SIZE(obj, size)
#else
  #define __Pyx_SET_REFCNT(obj, refcnt) Py_REFCNT(obj) = (refcnt)
  #define __Pyx_SET_SIZE(obj, size) Py_SIZE(obj) = (size)
#endif
#if CYTHON_ASSUME_SAFE_MACROS
  #define __Pyx_PySequence_ITEM(o, i) PySequence_ITEM(o, i)
  #define __Pyx_PySequence_SIZE(seq)  Py_SIZE(seq)
  #define __Pyx_PyTuple_SET_ITEM(o, i, v) (PyTuple_SET_ITEM(o, i, v), (0))
  #define __Pyx_PyList_SET_ITEM(o, i, v) (PyList_SET_ITEM(o, i, v), (0))
  #define __Pyx_PyTuple_GET_SIZE(o) PyTuple_GET_SIZE(o)
  #define __Pyx_PyList_GET_SIZE(o) PyList_GET_SIZE(o)
  #define __Pyx_PySet_GET_SIZE(o) PySet_GET_SIZE(o)
  #define __Pyx_PyBytes_GET_SIZE(o) PyBytes_GET_SIZE(o)
  #define __Pyx_PyByteArray_GET_SIZE(o) PyByteArray_GET_SIZE(o)
#else
  #define __Pyx_PySequence_ITEM(o, i) PySequence_GetItem(o, i)
  #define __Pyx_PySequence_SIZE(seq)  PySequence_Size(seq)
  #define __Pyx_PyTuple_SET_ITEM(o, i, v) PyTuple_SetItem(o, i, v)
  #define __Pyx_PyList_SET_ITEM(o, i, v) PyList_SetItem(o, i, v)
  #define __Pyx_PyTuple_GET_SIZE(o) PyTuple_Size(o)
  #define __Pyx_PyList_GET_SIZE(o) PyList_Size(o)
  #define __Pyx_PySet_GET_SIZE(o) PySet_Size(o)
  #define __Pyx_PyBytes_GET_SIZE(o) PyBytes_Size(o)
  #define __Pyx_PyByteArray_GET_SIZE(o) PyByteArray_Size(o)
#endif
#if PY_VERSION_HEX >= 0x030d00A1
  #define __Pyx_PyImport_AddModuleRef(name) PyImport_AddModuleRef(name)
#else
  static CYTHON_INLINE PyObject *__Pyx_PyImport_AddModuleRef(const char *name) {
      PyObject *module = PyImport_AddModule(name);
      Py_XINCREF(module);
      return module;
  }
#endif
#if PY_MAJOR_VERSION >= 3
  #define PyIntObject                  PyLongObject
  #define PyInt_Type                   PyLong_Type
  #define PyInt_Check(op)              PyLong_Check(op)
  #define PyInt_CheckExact(op)         PyLong_CheckExact(op)
  #define __Pyx_Py3Int_Check(op)       PyLong_Check(op)
  #define __Pyx_Py3Int_CheckExact(op)  PyLong_CheckExact(op)
  #define PyInt_FromString             PyLong_FromString
  #define PyInt_FromUnicode            PyLong_FromUnicode
  #define PyInt_FromLong               PyLong_FromLong
  #define PyInt_FromSize_t             PyLong_FromSize_t
  #define PyInt_FromSsize_t            PyLong_FromSsize_t
  #define PyInt_AsLong                 PyLong_AsLong
  #define PyInt_AS_LONG                PyLong_AS_LONG
  #define PyInt_AsSsize_t              PyLong_AsSsize_t
  #define PyInt_AsUnsignedLongMask     PyLong_AsUnsignedLongMask
  #define PyInt_AsUnsignedLongLongMask PyLong_AsUnsignedLongLongMask
  #define PyNumber_Int                 PyNumber_Long
#else
  #define __Pyx_Py3Int_Check(op)       (PyLong_Check(op) || PyInt_Check(op))
  #define __Pyx_Py3Int_CheckExact(op)  (PyLong_CheckExact(op) || PyInt_CheckExact(op))
#endif
#if PY_MAJOR_VERSION >= 3
  #define PyBoolObject                 PyLongObject
#endif
#if PY_MAJOR_VERSION >= 3 && CYTHON_COMPILING_IN_PYPY
  #ifndef PyUnicode_InternFromString
    #define PyUnicode_InternFromString(s) PyUnicode_FromString(s)
  #endif
#endif
#if PY_VERSION_HEX < 0x030200A4
  typedef long Py_hash_t;
  #define __Pyx_PyInt_FromHash_t PyInt_FromLong
  #define __Pyx_PyInt_AsHash_t   __Pyx_PyIndex_AsHash_t
#else
  #define __Pyx_PyInt_FromHash_t PyInt_FromSsize_t
  #define __Pyx_PyInt_AsHash_t   __Pyx_PyIndex_AsSsize_t
#endif
#if CYTHON_USE_ASYNC_SLOTS
  #if PY_VERSION_HEX >= 0x030500B1
    #define __Pyx_PyAsyncMethodsStruct PyAsyncMethods
    #define __Pyx_PyType_AsAsync(obj) (Py_TYPE(obj)->tp_as_async)
  #else
    #define __Pyx_PyType_AsAsync(obj) ((__Pyx_PyAsyncMethodsStruct*) (Py_TYPE(obj)->tp_reserved))
  #endif
#else
  #define __Pyx_PyType_AsAsync(obj) NULL
#endif
#ifndef __Pyx_PyAsyncMethodsStruct
    typedef struct {
        unaryfunc am_await;
        unaryfunc am_aiter;
        unaryfunc am_anext;
    } __Pyx_PyAsyncMethodsStruct;
#endif

#if defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)
  #if !defined(_USE_MATH_DEFINES)
    #define _USE_MATH_DEFINES
  #endif
#endif
#include <math.h>
#ifdef NAN
#define __PYX_NAN() ((float) NAN)
#else
static CYTHON_INLINE float __PYX_NAN() {
  float value;
  memset(&value, 0xFF, sizeof(value));
  return value;
}
#endif
#if defined(__CYGWIN__) && defined(_LDBL_EQ_DBL)
#define __Pyx_truncl trunc
#else
#define __Pyx_truncl truncl
#endif

#define __PYX_MARK_ERR_POS(f_index, lineno) \
    { __pyx_filename = __pyx_f[f_index]; (void)__pyx_filename; __pyx_lineno = lineno; (void)__pyx_lineno; __pyx_clineno = __LINE__; (void)__pyx_clineno; }
#define __PYX_ERR(f_index, lineno, Ln_error) \
    { __PYX_MARK_ERR_POS(f_index, lineno) goto Ln_error; }

#ifdef CYTHON_EXTERN_C
    #undef __PYX_EXTERN_C
    #define __PYX_EXTERN_C CYTHON_EXTERN_C
#elif defined(__PYX_EXTERN_C)
    #ifdef _MSC_VER
    #pragma message ("Please do not define the '__PYX_EXTERN_C' macro externally. Use 'CYTHON_EXTERN_C' instead.")
    #else
    #warning Please do not define the '__PYX_EXTERN_C' macro externally. Use 'CYTHON_EXTERN_C' instead.
    #endif
#else
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

#define __PYX_HAVE__qutk
#define __PYX_HAVE_API__qutk

#ifdef _OPENMP
#include <omp.h>
#endif 

#if defined(PYREX_WITHOUT_ASSERTIONS) && !defined(CYTHON_WITHOUT_ASSERTIONS)
#define CYTHON_WITHOUT_ASSERTIONS
#endif

typedef struct {PyObject **p; const char *s; const Py_ssize_t n; const char* encoding;
                const char is_unicode; const char is_str; const char intern; } __Pyx_StringTabEntry;

#define __PYX_DEFAULT_STRING_ENCODING_IS_ASCII 0
#define __PYX_DEFAULT_STRING_ENCODING_IS_UTF8 0
#define __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT (PY_MAJOR_VERSION >= 3 && __PYX_DEFAULT_STRING_ENCODING_IS_UTF8)
#define __PYX_DEFAULT_STRING_ENCODING ""
#define __Pyx_PyObject_FromString __Pyx_PyBytes_FromString
#define __Pyx_PyObject_FromStringAndSize __Pyx_PyBytes_FromStringAndSize
#define __Pyx_uchar_cast(c) ((unsigned char)c)
#define __Pyx_long_cast(x) ((long)x)
#define __Pyx_fits_Py_ssize_t(v, type, is_signed)  (\
    (sizeof(type) < sizeof(Py_ssize_t))  ||\
    (sizeof(type) > sizeof(Py_ssize_t) &&\
          likely(v < (type)PY_SSIZE_T_MAX ||\
                 v == (type)PY_SSIZE_T_MAX)  &&\
          (!is_signed || likely(v > (type)PY_SSIZE_T_MIN ||\
                                v == (type)PY_SSIZE_T_MIN)))  ||\
    (sizeof(type) == sizeof(Py_ssize_t) &&\
          (is_signed || likely(v < (type)PY_SSIZE_T_MAX ||\
                               v == (type)PY_SSIZE_T_MAX)))  )
static CYTHON_INLINE int __Pyx_is_valid_index(Py_ssize_t i, Py_ssize_t limit) {
    return (size_t) i < (size_t) limit;
}
#if defined (__cplusplus) && __cplusplus >= 201103L
    #include <cstdlib>
    #define __Pyx_sst_abs(value) std::abs(value)
#elif SIZEOF_INT >= SIZEOF_SIZE_T
    #define __Pyx_sst_abs(value) abs(value)
#elif SIZEOF_LONG >= SIZEOF_SIZE_T
    #define __Pyx_sst_abs(value) labs(value)
#elif defined (_MSC_VER)
    #define __Pyx_sst_abs(value) ((Py_ssize_t)_abs64(value))
#elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define __Pyx_sst_abs(value) llabs(value)
#elif defined (__GNUC__)
    #define __Pyx_sst_abs(value) __builtin_llabs(value)
#else
    #define __Pyx_sst_abs(value) ((value<0) ? -value : value)
#endif
static CYTHON_INLINE Py_ssize_t __Pyx_ssize_strlen(const char *s);
static CYTHON_INLINE const char* __Pyx_PyObject_AsString(PyObject*);
static CYTHON_INLINE const char* __Pyx_PyObject_AsStringAndSize(PyObject*, Py_ssize_t* length);
static CYTHON_INLINE PyObject* __Pyx_PyByteArray_FromString(const char*);
#define __Pyx_PyByteArray_FromStringAndSize(s, l) PyByteArray_FromStringAndSize((const char*)s, l)
#define __Pyx_PyBytes_FromString        PyBytes_FromString
#define __Pyx_PyBytes_FromStringAndSize PyBytes_FromStringAndSize
static CYTHON_INLINE PyObject* __Pyx_PyUnicode_FromString(const char*);
#if PY_MAJOR_VERSION < 3
    #define __Pyx_PyStr_FromString        __Pyx_PyBytes_FromString
    #define __Pyx_PyStr_FromStringAndSize __Pyx_PyBytes_FromStringAndSize
#else
    #define __Pyx_PyStr_FromString        __Pyx_PyUnicode_FromString
    #define __Pyx_PyStr_FromStringAndSize __Pyx_PyUnicode_FromStringAndSize
#endif
#define __Pyx_PyBytes_AsWritableString(s)     ((char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsWritableSString(s)    ((signed char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsWritableUString(s)    ((unsigned char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsString(s)     ((const char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsSString(s)    ((const signed char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsUString(s)    ((const unsigned char*) PyBytes_AS_STRING(s))
#define __Pyx_PyObject_AsWritableString(s)    ((char*)(__pyx_uintptr_t) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsWritableSString(s)    ((signed char*)(__pyx_uintptr_t) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsWritableUString(s)    ((unsigned char*)(__pyx_uintptr_t) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsSString(s)    ((const signed char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsUString(s)    ((const unsigned char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_FromCString(s)  __Pyx_PyObject_FromString((const char*)s)
#define __Pyx_PyBytes_FromCString(s)   __Pyx_PyBytes_FromString((const char*)s)
#define __Pyx_PyByteArray_FromCString(s)   __Pyx_PyByteArray_FromString((const char*)s)
#define __Pyx_PyStr_FromCString(s)     __Pyx_PyStr_FromString((const char*)s)
#define __Pyx_PyUnicode_FromCString(s) __Pyx_PyUnicode_FromString((const char*)s)
#if CYTHON_COMPILING_IN_LIMITED_API
static CYTHON_INLINE size_t __Pyx_Py_UNICODE_strlen(const wchar_t *u)
{
    const wchar_t *u_end = u;
    while (*u_end++) ;
    return (size_t)(u_end - u - 1);
}
#else
static CYTHON_INLINE size_t __Pyx_Py_UNICODE_strlen(const Py_UNICODE *u)
{
    const Py_UNICODE *u_end = u;
    while (*u_end++) ;
    return (size_t)(u_end - u - 1);
}
#endif
#define __Pyx_PyUnicode_FromOrdinal(o)       PyUnicode_FromOrdinal((int)o)
#define __Pyx_PyUnicode_FromUnicode(u)       PyUnicode_FromUnicode(u, __Pyx_Py_UNICODE_strlen(u))
#define __Pyx_PyUnicode_FromUnicodeAndLength PyUnicode_FromUnicode
#define __Pyx_PyUnicode_AsUnicode            PyUnicode_AsUnicode
#define __Pyx_NewRef(obj) (Py_INCREF(obj), obj)
#define __Pyx_Owned_Py_None(b) __Pyx_NewRef(Py_None)
static CYTHON_INLINE PyObject * __Pyx_PyBool_FromLong(long b);
static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject*);
static CYTHON_INLINE int __Pyx_PyObject_IsTrueAndDecref(PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyNumber_IntOrLong(PyObject* x);
#define __Pyx_PySequence_Tuple(obj)\
    (likely(PyTuple_CheckExact(obj)) ? __Pyx_NewRef(obj) : PySequence_Tuple(obj))
static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject*);
static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t);
static CYTHON_INLINE Py_hash_t __Pyx_PyIndex_AsHash_t(PyObject*);
#if CYTHON_ASSUME_SAFE_MACROS
#define __pyx_PyFloat_AsDouble(x) (PyFloat_CheckExact(x) ? PyFloat_AS_DOUBLE(x) : PyFloat_AsDouble(x))
#else
#define __pyx_PyFloat_AsDouble(x) PyFloat_AsDouble(x)
#endif
#define __pyx_PyFloat_AsFloat(x) ((float) __pyx_PyFloat_AsDouble(x))
#if PY_MAJOR_VERSION >= 3
#define __Pyx_PyNumber_Int(x) (PyLong_CheckExact(x) ? __Pyx_NewRef(x) : PyNumber_Long(x))
#else
#define __Pyx_PyNumber_Int(x) (PyInt_CheckExact(x) ? __Pyx_NewRef(x) : PyNumber_Int(x))
#endif
#if CYTHON_USE_PYLONG_INTERNALS
  #if PY_VERSION_HEX >= 0x030C00A7
  #ifndef _PyLong_SIGN_MASK
    #define _PyLong_SIGN_MASK 3
  #endif
  #ifndef _PyLong_NON_SIZE_BITS
    #define _PyLong_NON_SIZE_BITS 3
  #endif
  #define __Pyx_PyLong_Sign(x)  (((PyLongObject*)x)->long_value.lv_tag & _PyLong_SIGN_MASK)
  #define __Pyx_PyLong_IsNeg(x)  ((__Pyx_PyLong_Sign(x) & 2) != 0)
  #define __Pyx_PyLong_IsNonNeg(x)  (!__Pyx_PyLong_IsNeg(x))
  #define __Pyx_PyLong_IsZero(x)  (__Pyx_PyLong_Sign(x) & 1)
  #define __Pyx_PyLong_IsPos(x)  (__Pyx_PyLong_Sign(x) == 0)
  #define __Pyx_PyLong_CompactValueUnsigned(x)  (__Pyx_PyLong_Digits(x)[0])
  #define __Pyx_PyLong_DigitCount(x)  ((Py_ssize_t) (((PyLongObject*)x)->long_value.lv_tag >> _PyLong_NON_SIZE_BITS))
  #define __Pyx_PyLong_SignedDigitCount(x)\
        ((1 - (Py_ssize_t) __Pyx_PyLong_Sign(x)) * __Pyx_PyLong_DigitCount(x))
  #if defined(PyUnstable_Long_IsCompact) && defined(PyUnstable_Long_CompactValue)
    #define __Pyx_PyLong_IsCompact(x)     PyUnstable_Long_IsCompact((PyLongObject*) x)
    #define __Pyx_PyLong_CompactValue(x)  PyUnstable_Long_CompactValue((PyLongObject*) x)
  #else
    #define __Pyx_PyLong_IsCompact(x)     (((PyLongObject*)x)->long_value.lv_tag < (2 << _PyLong_NON_SIZE_BITS))
    #define __Pyx_PyLong_CompactValue(x)  ((1 - (Py_ssize_t) __Pyx_PyLong_Sign(x)) * (Py_ssize_t) __Pyx_PyLong_Digits(x)[0])
  #endif
  typedef Py_ssize_t  __Pyx_compact_pylong;
  typedef size_t  __Pyx_compact_upylong;
  #else  // Py < 3.12
  #define __Pyx_PyLong_IsNeg(x)  (Py_SIZE(x) < 0)
  #define __Pyx_PyLong_IsNonNeg(x)  (Py_SIZE(x) >= 0)
  #define __Pyx_PyLong_IsZero(x)  (Py_SIZE(x) == 0)
  #define __Pyx_PyLong_IsPos(x)  (Py_SIZE(x) > 0)
  #define __Pyx_PyLong_CompactValueUnsigned(x)  ((Py_SIZE(x) == 0) ? 0 : __Pyx_PyLong_Digits(x)[0])
  #define __Pyx_PyLong_DigitCount(x)  __Pyx_sst_abs(Py_SIZE(x))
  #define __Pyx_PyLong_SignedDigitCount(x)  Py_SIZE(x)
  #define __Pyx_PyLong_IsCompact(x)  (Py_SIZE(x) == 0 || Py_SIZE(x) == 1 || Py_SIZE(x) == -1)
  #define __Pyx_PyLong_CompactValue(x)\
        ((Py_SIZE(x) == 0) ? (sdigit) 0 : ((Py_SIZE(x) < 0) ? -(sdigit)__Pyx_PyLong_Digits(x)[0] : (sdigit)__Pyx_PyLong_Digits(x)[0]))
  typedef sdigit  __Pyx_compact_pylong;
  typedef digit  __Pyx_compact_upylong;
  #endif
  #if PY_VERSION_HEX >= 0x030C00A5
  #define __Pyx_PyLong_Digits(x)  (((PyLongObject*)x)->long_value.ob_digit)
  #else
  #define __Pyx_PyLong_Digits(x)  (((PyLongObject*)x)->ob_digit)
  #endif
#endif
#if PY_MAJOR_VERSION < 3 && __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
#include <string.h>
static int __Pyx_sys_getdefaultencoding_not_ascii;
static int __Pyx_init_sys_getdefaultencoding_params(void) {
    PyObject* sys;
    PyObject* default_encoding = NULL;
    PyObject* ascii_chars_u = NULL;
    PyObject* ascii_chars_b = NULL;
    const char* default_encoding_c;
    sys = PyImport_ImportModule("sys");
    if (!sys) goto bad;
    default_encoding = PyObject_CallMethod(sys, (char*) "getdefaultencoding", NULL);
    Py_DECREF(sys);
    if (!default_encoding) goto bad;
    default_encoding_c = PyBytes_AsString(default_encoding);
    if (!default_encoding_c) goto bad;
    if (strcmp(default_encoding_c, "ascii") == 0) {
        __Pyx_sys_getdefaultencoding_not_ascii = 0;
    } else {
        char ascii_chars[128];
        int c;
        for (c = 0; c < 128; c++) {
            ascii_chars[c] = (char) c;
        }
        __Pyx_sys_getdefaultencoding_not_ascii = 1;
        ascii_chars_u = PyUnicode_DecodeASCII(ascii_chars, 128, NULL);
        if (!ascii_chars_u) goto bad;
        ascii_chars_b = PyUnicode_AsEncodedString(ascii_chars_u, default_encoding_c, NULL);
        if (!ascii_chars_b || !PyBytes_Check(ascii_chars_b) || memcmp(ascii_chars, PyBytes_AS_STRING(ascii_chars_b), 128) != 0) {
            PyErr_Format(
                PyExc_ValueError,
                "This module compiled with c_string_encoding=ascii, but default encoding '%.200s' is not a superset of ascii.",
                default_encoding_c);
            goto bad;
        }
        Py_DECREF(ascii_chars_u);
        Py_DECREF(ascii_chars_b);
    }
    Py_DECREF(default_encoding);
    return 0;
bad:
    Py_XDECREF(default_encoding);
    Py_XDECREF(ascii_chars_u);
    Py_XDECREF(ascii_chars_b);
    return -1;
}
#endif
#if __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT && PY_MAJOR_VERSION >= 3
#define __Pyx_PyUnicode_FromStringAndSize(c_str, size) PyUnicode_DecodeUTF8(c_str, size, NULL)
#else
#define __Pyx_PyUnicode_FromStringAndSize(c_str, size) PyUnicode_Decode(c_str, size, __PYX_DEFAULT_STRING_ENCODING, NULL)
#if __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT
#include <string.h>
static char* __PYX_DEFAULT_STRING_ENCODING;
static int __Pyx_init_sys_getdefaultencoding_params(void) {
    PyObject* sys;
    PyObject* default_encoding = NULL;
    char* default_encoding_c;
    sys = PyImport_ImportModule("sys");
    if (!sys) goto bad;
    default_encoding = PyObject_CallMethod(sys, (char*) (const char*) "getdefaultencoding", NULL);
    Py_DECREF(sys);
    if (!default_encoding) goto bad;
    default_encoding_c = PyBytes_AsString(default_encoding);
    if (!default_encoding_c) goto bad;
    __PYX_DEFAULT_STRING_ENCODING = (char*) malloc(strlen(default_encoding_c) + 1);
    if (!__PYX_DEFAULT_STRING_ENCODING) goto bad;
    strcpy(__PYX_DEFAULT_STRING_ENCODING, default_encoding_c);
    Py_DECREF(default_encoding);
    return 0;
bad:
    Py_XDECREF(default_encoding);
    return -1;
}
#endif
#endif



#if defined(__GNUC__)     && (__GNUC__ > 2 || (__GNUC__ == 2 && (__GNUC_MINOR__ > 95)))
  #define likely(x)   __builtin_expect(!!(x), 1)
  #define unlikely(x) __builtin_expect(!!(x), 0)
#else 
  #define likely(x)   (x)
  #define unlikely(x) (x)
#endif 
static CYTHON_INLINE void __Pyx_pretend_to_initialize(void* ptr) { (void)ptr; }

#if !CYTHON_USE_MODULE_STATE
static PyObject *__pyx_m = NULL;
#endif
static int __pyx_lineno;
static int __pyx_clineno = 0;
static const char * __pyx_cfilenm = __FILE__;
static const char *__pyx_filename;



static const char *__pyx_f[] = {
  "qutk.py",
};


#ifndef __PYX_FORCE_INIT_THREADS
  #define __PYX_FORCE_INIT_THREADS 0
#endif






struct __pyx_obj_4qutk___pyx_scope_struct__index;
struct __pyx_obj_4qutk___pyx_scope_struct_1_miu;


struct __pyx_obj_4qutk___pyx_scope_struct__index {
  PyObject_HEAD
  PyObject *__pyx_v_P0;
  PyObject *__pyx_Uv__peg;
};



struct __pyx_obj_4qutk___pyx_scope_struct_1_miu {
  PyObject_HEAD
  PyObject *__pyx_v_k;
  PyObject *__pyx_v_server_cost;
  PyObject *__pyx_v_server_income;
  PyObject *__pyx_Uv__5cg;
};





#ifndef CYTHON_REFNANNY
  #define CYTHON_REFNANNY 0
#endif
#if CYTHON_REFNANNY
  typedef struct {
    void (*INCREF)(void*, PyObject*, Py_ssize_t);
    void (*DECREF)(void*, PyObject*, Py_ssize_t);
    void (*GOTREF)(void*, PyObject*, Py_ssize_t);
    void (*GIVEREF)(void*, PyObject*, Py_ssize_t);
    void* (*SetupContext)(const char*, Py_ssize_t, const char*);
    void (*FinishContext)(void**);
  } __Pyx_RefNannyAPIStruct;
  static __Pyx_RefNannyAPIStruct *__Pyx_RefNanny = NULL;
  static __Pyx_RefNannyAPIStruct *__Pyx_RefNannyImportAPI(const char *modname);
  #define __Pyx_RefNannyDeclarations void *__pyx_refnanny = NULL;
#ifdef WITH_THREAD
  #define __Pyx_RefNannySetupContext(name, acquire_gil)\
          if (acquire_gil) {\
              PyGILState_STATE __pyx_gilstate_save = PyGILState_Ensure();\
              __pyx_refnanny = __Pyx_RefNanny->SetupContext((name), (__LINE__), (__FILE__));\
              PyGILState_Release(__pyx_gilstate_save);\
          } else {\
              __pyx_refnanny = __Pyx_RefNanny->SetupContext((name), (__LINE__), (__FILE__));\
          }
  #define __Pyx_RefNannyFinishContextNogil() {\
              PyGILState_STATE __pyx_gilstate_save = PyGILState_Ensure();\
              __Pyx_RefNannyFinishContext();\
              PyGILState_Release(__pyx_gilstate_save);\
          }
#else
  #define __Pyx_RefNannySetupContext(name, acquire_gil)\
          __pyx_refnanny = __Pyx_RefNanny->SetupContext((name), (__LINE__), (__FILE__))
  #define __Pyx_RefNannyFinishContextNogil() __Pyx_RefNannyFinishContext()
#endif
  #define __Pyx_RefNannyFinishContextNogil() {\
              PyGILState_STATE __pyx_gilstate_save = PyGILState_Ensure();\
              __Pyx_RefNannyFinishContext();\
              PyGILState_Release(__pyx_gilstate_save);\
          }
  #define __Pyx_RefNannyFinishContext()\
          __Pyx_RefNanny->FinishContext(&__pyx_refnanny)
  #define __Pyx_INCREF(r)  __Pyx_RefNanny->INCREF(__pyx_refnanny, (PyObject *)(r), (__LINE__))
  #define __Pyx_DECREF(r)  __Pyx_RefNanny->DECREF(__pyx_refnanny, (PyObject *)(r), (__LINE__))
  #define __Pyx_GOTREF(r)  __Pyx_RefNanny->GOTREF(__pyx_refnanny, (PyObject *)(r), (__LINE__))
  #define __Pyx_GIVEREF(r) __Pyx_RefNanny->GIVEREF(__pyx_refnanny, (PyObject *)(r), (__LINE__))
  #define __Pyx_XINCREF(r)  do { if((r) == NULL); else {__Pyx_INCREF(r); }} while(0)
  #define __Pyx_XDECREF(r)  do { if((r) == NULL); else {__Pyx_DECREF(r); }} while(0)
  #define __Pyx_XGOTREF(r)  do { if((r) == NULL); else {__Pyx_GOTREF(r); }} while(0)
  #define __Pyx_XGIVEREF(r) do { if((r) == NULL); else {__Pyx_GIVEREF(r);}} while(0)
#else
  #define __Pyx_RefNannyDeclarations
  #define __Pyx_RefNannySetupContext(name, acquire_gil)
  #define __Pyx_RefNannyFinishContextNogil()
  #define __Pyx_RefNannyFinishContext()
  #define __Pyx_INCREF(r) Py_INCREF(r)
  #define __Pyx_DECREF(r) Py_DECREF(r)
  #define __Pyx_GOTREF(r)
  #define __Pyx_GIVEREF(r)
  #define __Pyx_XINCREF(r) Py_XINCREF(r)
  #define __Pyx_XDECREF(r) Py_XDECREF(r)
  #define __Pyx_XGOTREF(r)
  #define __Pyx_XGIVEREF(r)
#endif
#define __Pyx_Py_XDECREF_SET(r, v) do {\
        PyObject *tmp = (PyObject *) r;\
        r = v; Py_XDECREF(tmp);\
    } while (0)
#define __Pyx_XDECREF_SET(r, v) do {\
        PyObject *tmp = (PyObject *) r;\
        r = v; __Pyx_XDECREF(tmp);\
    } while (0)
#define __Pyx_DECREF_SET(r, v) do {\
        PyObject *tmp = (PyObject *) r;\
        r = v; __Pyx_DECREF(tmp);\
    } while (0)
#define __Pyx_CLEAR(r)    do { PyObject* tmp = ((PyObject*)(r)); r = NULL; __Pyx_DECREF(tmp);} while(0)
#define __Pyx_XCLEAR(r)   do { if((r) != NULL) {PyObject* tmp = ((PyObject*)(r)); r = NULL; __Pyx_DECREF(tmp);}} while(0)


#if CYTHON_FAST_THREAD_STATE
#define __Pyx_PyErr_ExceptionMatches(err) __Pyx_PyErr_ExceptionMatchesInState(__pyx_tstate, err)
static CYTHON_INLINE int __Pyx_PyErr_ExceptionMatchesInState(PyThreadState* tstate, PyObject* err);
#else
#define __Pyx_PyErr_ExceptionMatches(err)  PyErr_ExceptionMatches(err)
#endif


#if CYTHON_FAST_THREAD_STATE
#define __Pyx_PyThreadState_declare  PyThreadState *__pyx_tstate;
#define __Pyx_PyThreadState_assign  __pyx_tstate = __Pyx_PyThreadState_Current;
#if PY_VERSION_HEX >= 0x030C00A6
#define __Pyx_PyErr_Occurred()  (__pyx_tstate->current_exception != NULL)
#define __Pyx_PyErr_CurrentExceptionType()  (__pyx_tstate->current_exception ? (PyObject*) Py_TYPE(__pyx_tstate->current_exception) : (PyObject*) NULL)
#else
#define __Pyx_PyErr_Occurred()  (__pyx_tstate->curexc_type != NULL)
#define __Pyx_PyErr_CurrentExceptionType()  (__pyx_tstate->curexc_type)
#endif
#else
#define __Pyx_PyThreadState_declare
#define __Pyx_PyThreadState_assign
#define __Pyx_PyErr_Occurred()  (PyErr_Occurred() != NULL)
#define __Pyx_PyErr_CurrentExceptionType()  PyErr_Occurred()
#endif


#if CYTHON_FAST_THREAD_STATE
#define __Pyx_PyErr_Clear() __Pyx_ErrRestore(NULL, NULL, NULL)
#define __Pyx_ErrRestoreWithState(type, value, tb)  __Pyx_ErrRestoreInState(PyThreadState_GET(), type, value, tb)
#define __Pyx_ErrFetchWithState(type, value, tb)    __Pyx_ErrFetchInState(PyThreadState_GET(), type, value, tb)
#define __Pyx_ErrRestore(type, value, tb)  __Pyx_ErrRestoreInState(__pyx_tstate, type, value, tb)
#define __Pyx_ErrFetch(type, value, tb)    __Pyx_ErrFetchInState(__pyx_tstate, type, value, tb)
static CYTHON_INLINE void __Pyx_ErrRestoreInState(PyThreadState *tstate, PyObject *type, PyObject *value, PyObject *tb);
static CYTHON_INLINE void __Pyx_ErrFetchInState(PyThreadState *tstate, PyObject **type, PyObject **value, PyObject **tb);
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030C00A6
#define __Pyx_PyErr_SetNone(exc) (Py_INCREF(exc), __Pyx_ErrRestore((exc), NULL, NULL))
#else
#define __Pyx_PyErr_SetNone(exc) PyErr_SetNone(exc)
#endif
#else
#define __Pyx_PyErr_Clear() PyErr_Clear()
#define __Pyx_PyErr_SetNone(exc) PyErr_SetNone(exc)
#define __Pyx_ErrRestoreWithState(type, value, tb)  PyErr_Restore(type, value, tb)
#define __Pyx_ErrFetchWithState(type, value, tb)  PyErr_Fetch(type, value, tb)
#define __Pyx_ErrRestoreInState(tstate, type, value, tb)  PyErr_Restore(type, value, tb)
#define __Pyx_ErrFetchInState(tstate, type, value, tb)  PyErr_Fetch(type, value, tb)
#define __Pyx_ErrRestore(type, value, tb)  PyErr_Restore(type, value, tb)
#define __Pyx_ErrFetch(type, value, tb)  PyErr_Fetch(type, value, tb)
#endif


#if CYTHON_USE_TYPE_SLOTS
static CYTHON_INLINE PyObject* __Pyx_PyObject_GetAttrStr(PyObject* obj, PyObject* attr_name);
#else
#define __Pyx_PyObject_GetAttrStr(o,n) PyObject_GetAttr(o,n)
#endif


static CYTHON_INLINE PyObject* __Pyx_PyObject_GetAttrStrNoError(PyObject* obj, PyObject* attr_name);


static PyObject *__Pyx_GetBuiltinName(PyObject *name);


#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyList_FromArray(PyObject *const *src, Py_ssize_t n);
static CYTHON_INLINE PyObject* __Pyx_PyTuple_FromArray(PyObject *const *src, Py_ssize_t n);
#endif


#include <string.h>


static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals);


static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals);


#if CYTHON_AVOID_BORROWED_REFS
    #define __Pyx_Arg_VARARGS(args, i) PySequence_GetItem(args, i)
#elif CYTHON_ASSUME_SAFE_MACROS
    #define __Pyx_Arg_VARARGS(args, i) PyTuple_GET_ITEM(args, i)
#else
    #define __Pyx_Arg_VARARGS(args, i) PyTuple_GetItem(args, i)
#endif
#if CYTHON_AVOID_BORROWED_REFS
    #define __Pyx_Arg_NewRef_VARARGS(arg) __Pyx_NewRef(arg)
    #define __Pyx_Arg_XDECREF_VARARGS(arg) Py_XDECREF(arg)
#else
    #define __Pyx_Arg_NewRef_VARARGS(arg) arg // no-op
    #define __Pyx_Arg_XDECREF_VARARGS(arg) // no-op - arg is borrowed
#endif
#define __Pyx_NumKwargs_VARARGS(kwds) PyDict_Size(kwds)
#define __Pyx_KwValues_VARARGS(args, nargs) NULL
#define __Pyx_GetKwValue_VARARGS(kw, kwvalues, s) __Pyx_PyDict_GetItemStrWithError(kw, s)
#define __Pyx_KwargsAsDict_VARARGS(kw, kwvalues) PyDict_Copy(kw)
#if CYTHON_METH_FASTCALL
    #define __Pyx_Arg_FASTCALL(args, i) args[i]
    #define __Pyx_NumKwargs_FASTCALL(kwds) PyTuple_GET_SIZE(kwds)
    #define __Pyx_KwValues_FASTCALL(args, nargs) ((args) + (nargs))
    static CYTHON_INLINE PyObject * __Pyx_GetKwValue_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues, PyObject *s);
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000
    CYTHON_UNUSED static PyObject *__Pyx_KwargsAsDict_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues);
  #else
    #define __Pyx_KwargsAsDict_FASTCALL(kw, kwvalues) _PyStack_AsDict(kwvalues, kw)
  #endif
    #define __Pyx_Arg_NewRef_FASTCALL(arg) arg // no-op, __Pyx_Arg_FASTCALL is direct and this needs
    #define __Pyx_Arg_XDECREF_FASTCALL(arg)  // no-op - arg was returned from array
#else
    #define __Pyx_Arg_FASTCALL __Pyx_Arg_VARARGS
    #define __Pyx_NumKwargs_FASTCALL __Pyx_NumKwargs_VARARGS
    #define __Pyx_KwValues_FASTCALL __Pyx_KwValues_VARARGS
    #define __Pyx_GetKwValue_FASTCALL __Pyx_GetKwValue_VARARGS
    #define __Pyx_KwargsAsDict_FASTCALL __Pyx_KwargsAsDict_VARARGS
    #define __Pyx_Arg_NewRef_FASTCALL(arg) __Pyx_Arg_NewRef_VARARGS(arg)
    #define __Pyx_Arg_XDECREF_FASTCALL(arg) __Pyx_Arg_XDECREF_VARARGS(arg)
#endif
#if CYTHON_COMPILING_IN_CPYTHON && CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
#define __Pyx_ArgsSlice_VARARGS(args, start, stop) __Pyx_PyTuple_FromArray(&__Pyx_Arg_VARARGS(args, start), stop - start)
#define __Pyx_ArgsSlice_FASTCALL(args, start, stop) __Pyx_PyTuple_FromArray(&__Pyx_Arg_FASTCALL(args, start), stop - start)
#else
#define __Pyx_ArgsSlice_VARARGS(args, start, stop) PyTuple_GetSlice(args, start, stop)
#define __Pyx_ArgsSlice_FASTCALL(args, start, stop) PyTuple_GetSlice(args, start, stop)
#endif


static void __Pyx_RaiseArgtupleInvalid(const char* func_name, int exact,
    Py_ssize_t num_min, Py_ssize_t num_max, Py_ssize_t num_found);


static void __Pyx_RaiseDoubleKeywordsError(const char* func_name, PyObject* kw_name);


static int __Pyx_ParseOptionalKeywords(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    PyObject *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name);


static CYTHON_INLINE void __Pyx_RaiseClosureNameError(const char *varname);


#if CYTHON_USE_DICT_VERSIONS && CYTHON_USE_TYPE_SLOTS
#define __PYX_DICT_VERSION_INIT  ((PY_UINT64_T) -1)
#define __PYX_GET_DICT_VERSION(dict)  (((PyDictObject*)(dict))->ma_version_tag)
#define __PYX_UPDATE_DICT_CACHE(dict, value, cache_var, version_var)\
    (version_var) = __PYX_GET_DICT_VERSION(dict);\
    (cache_var) = (value);
#define __PYX_PY_DICT_LOOKUP_IF_MODIFIED(VAR, DICT, LOOKUP) {\
    static PY_UINT64_T __pyx_dict_version = 0;\
    static PyObject *__pyx_dict_cached_value = NULL;\
    if (likely(__PYX_GET_DICT_VERSION(DICT) == __pyx_dict_version)) {\
        (VAR) = __pyx_dict_cached_value;\
    } else {\
        (VAR) = __pyx_dict_cached_value = (LOOKUP);\
        __pyx_dict_version = __PYX_GET_DICT_VERSION(DICT);\
    }\
}
static CYTHON_INLINE PY_UINT64_T __Pyx_get_tp_dict_version(PyObject *obj);
static CYTHON_INLINE PY_UINT64_T __Pyx_get_object_dict_version(PyObject *obj);
static CYTHON_INLINE int __Pyx_object_dict_version_matches(PyObject* obj, PY_UINT64_T tp_dict_version, PY_UINT64_T obj_dict_version);
#else
#define __PYX_GET_DICT_VERSION(dict)  (0)
#define __PYX_UPDATE_DICT_CACHE(dict, value, cache_var, version_var)
#define __PYX_PY_DICT_LOOKUP_IF_MODIFIED(VAR, DICT, LOOKUP)  (VAR) = (LOOKUP);
#endif


#if CYTHON_USE_DICT_VERSIONS
#define __Pyx_GetModuleGlobalName(var, name)  do {\
    static PY_UINT64_T __pyx_dict_version = 0;\
    static PyObject *__pyx_dict_cached_value = NULL;\
    (var) = (likely(__pyx_dict_version == __PYX_GET_DICT_VERSION(__pyx_d))) ?\
        (likely(__pyx_dict_cached_value) ? __Pyx_NewRef(__pyx_dict_cached_value) : __Pyx_GetBuiltinName(name)) :\
        __Pyx__GetModuleGlobalName(name, &__pyx_dict_version, &__pyx_dict_cached_value);\
} while(0)
#define __Pyx_GetModuleGlobalNameUncached(var, name)  do {\
    PY_UINT64_T __pyx_dict_version;\
    PyObject *__pyx_dict_cached_value;\
    (var) = __Pyx__GetModuleGlobalName(name, &__pyx_dict_version, &__pyx_dict_cached_value);\
} while(0)
static PyObject *__Pyx__GetModuleGlobalName(PyObject *name, PY_UINT64_T *dict_version, PyObject **dict_cached_value);
#else
#define __Pyx_GetModuleGlobalName(var, name)  (var) = __Pyx__GetModuleGlobalName(name)
#define __Pyx_GetModuleGlobalNameUncached(var, name)  (var) = __Pyx__GetModuleGlobalName(name)
static CYTHON_INLINE PyObject *__Pyx__GetModuleGlobalName(PyObject *name);
#endif


#if CYTHON_FAST_PYCALL
#if !CYTHON_VECTORCALL
#define __Pyx_PyFunction_FastCall(func, args, nargs)\
    __Pyx_PyFunction_FastCallDict((func), (args), (nargs), NULL)
static PyObject *__Pyx_PyFunction_FastCallDict(PyObject *func, PyObject **args, Py_ssize_t nargs, PyObject *kwargs);
#endif
#define __Pyx_BUILD_ASSERT_EXPR(cond)\
    (sizeof(char [1 - 2*!(cond)]) - 1)
#ifndef Py_MEMBER_SIZE
#define Py_MEMBER_SIZE(type, member) sizeof(((type *)0)->member)
#endif
#if !CYTHON_VECTORCALL
#if PY_VERSION_HEX >= 0x03080000
  #include "frameobject.h"
#if PY_VERSION_HEX >= 0x030b00a6 && !CYTHON_COMPILING_IN_LIMITED_API
  #ifndef Py_BUILD_CORE
    #define Py_BUILD_CORE 1
  #endif
  #include "internal/pycore_frame.h"
#endif
  #define __Pxy_PyFrame_Initialize_Offsets()
  #define __Pyx_PyFrame_GetLocalsplus(frame)  ((frame)->f_localsplus)
#else
  static size_t __pyx_pyframe_localsplus_offset = 0;
  #include "frameobject.h"
  #define __Pxy_PyFrame_Initialize_Offsets()\
    ((void)__Pyx_BUILD_ASSERT_EXPR(sizeof(PyFrameObject) == offsetof(PyFrameObject, f_localsplus) + Py_MEMBER_SIZE(PyFrameObject, f_localsplus)),\
     (void)(__pyx_pyframe_localsplus_offset = ((size_t)PyFrame_Type.tp_basicsize) - Py_MEMBER_SIZE(PyFrameObject, f_localsplus)))
  #define __Pyx_PyFrame_GetLocalsplus(frame)\
    (assert(__pyx_pyframe_localsplus_offset), (PyObject **)(((char *)(frame)) + __pyx_pyframe_localsplus_offset))
#endif
#endif
#endif


#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_Call(PyObject *func, PyObject *arg, PyObject *kw);
#else
#define __Pyx_PyObject_Call(func, arg, kw) PyObject_Call(func, arg, kw)
#endif


#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallMethO(PyObject *func, PyObject *arg);
#endif


#define __Pyx_PyObject_FastCall(func, args, nargs)  __Pyx_PyObject_FastCallDict(func, args, (size_t)(nargs), NULL)
static CYTHON_INLINE PyObject* __Pyx_PyObject_FastCallDict(PyObject *func, PyObject **args, size_t nargs, PyObject *kwargs);


static CYTHON_INLINE PyObject* __Pyx_PyObject_GetSlice(
        PyObject* obj, Py_ssize_t cstart, Py_ssize_t cstop,
        PyObject** py_start, PyObject** py_stop, PyObject** py_slice,
        int has_cstart, int has_cstop, int wraparound);


static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(Py_ssize_t expected);


static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index);


static CYTHON_INLINE int __Pyx_IterFinish(void);


static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected);


#include <structmember.h>


#if CYTHON_USE_TYPE_SPECS
static int __Pyx_fix_up_extension_type_from_spec(PyType_Spec *spec, PyTypeObject *type);
#endif


static PyObject *__Pyx_FetchSharedCythonABIModule(void);


#if !CYTHON_USE_TYPE_SPECS
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);
#else
static PyTypeObject* __Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases);
#endif


#if CYTHON_COMPILING_IN_LIMITED_API
static PyObject *__Pyx_PyMethod_New(PyObject *func, PyObject *self, PyObject *typ) {
    PyObject *typesModule=NULL, *methodType=NULL, *result=NULL;
    CYTHON_UNUSED_VAR(typ);
    if (!self)
        return __Pyx_NewRef(func);
    typesModule = PyImport_ImportModule("types");
    if (!typesModule) return NULL;
    methodType = PyObject_GetAttrString(typesModule, "MethodType");
    Py_DECREF(typesModule);
    if (!methodType) return NULL;
    result = PyObject_CallFunctionObjArgs(methodType, func, self, NULL);
    Py_DECREF(methodType);
    return result;
}
#elif PY_MAJOR_VERSION >= 3
static PyObject *__Pyx_PyMethod_New(PyObject *func, PyObject *self, PyObject *typ) {
    CYTHON_UNUSED_VAR(typ);
    if (!self)
        return __Pyx_NewRef(func);
    return PyMethod_New(func, self);
}
#else
    #define __Pyx_PyMethod_New PyMethod_New
#endif


#if CYTHON_METH_FASTCALL
static CYTHON_INLINE PyObject *__Pyx_PyVectorcall_FastCallDict(PyObject *func, __pyx_vectorcallfunc vc, PyObject *const *args, size_t nargs, PyObject *kw);
#endif


#define __Pyx_CyFunction_USED
#define __Pyx_CYFUNCTION_STATICMETHOD  0x01
#define __Pyx_CYFUNCTION_CLASSMETHOD   0x02
#define __Pyx_CYFUNCTION_CCLASS        0x04
#define __Pyx_CYFUNCTION_COROUTINE     0x08
#define __Pyx_CyFunction_GetClosure(f)\
    (((__pyx_CyFunctionObject *) (f))->func_closure)
#if PY_VERSION_HEX < 0x030900B1 || CYTHON_COMPILING_IN_LIMITED_API
  #define __Pyx_CyFunction_GetClassObj(f)\
      (((__pyx_CyFunctionObject *) (f))->func_classobj)
#else
  #define __Pyx_CyFunction_GetClassObj(f)\
      ((PyObject*) ((PyCMethodObject *) (f))->mm_class)
#endif
#define __Pyx_CyFunction_SetClassObj(f, classobj)\
    __Pyx__CyFunction_SetClassObj((__pyx_CyFunctionObject *) (f), (classobj))
#define __Pyx_CyFunction_Defaults(type, f)\
    ((type *)(((__pyx_CyFunctionObject *) (f))->defaults))
#define __Pyx_CyFunction_SetDefaultsGetter(f, g)\
    ((__pyx_CyFunctionObject *) (f))->defaults_getter = (g)
typedef struct {
#if CYTHON_COMPILING_IN_LIMITED_API
    PyObject_HEAD
    PyObject *func;
#elif PY_VERSION_HEX < 0x030900B1
    PyCFunctionObject func;
#else
    PyCMethodObject func;
#endif
#if CYTHON_BACKPORT_VECTORCALL
    __pyx_vectorcallfunc func_vectorcall;
#endif
#if PY_VERSION_HEX < 0x030500A0 || CYTHON_COMPILING_IN_LIMITED_API
    PyObject *func_weakreflist;
#endif
    PyObject *func_dict;
    PyObject *func_name;
    PyObject *func_qualname;
    PyObject *func_doc;
    PyObject *func_globals;
    PyObject *func_code;
    PyObject *func_closure;
#if PY_VERSION_HEX < 0x030900B1 || CYTHON_COMPILING_IN_LIMITED_API
    PyObject *func_classobj;
#endif
    void *defaults;
    int defaults_pyobjects;
    size_t defaults_size;  // used by FusedFunction for copying defaults
    int flags;
    PyObject *defaults_tuple;
    PyObject *defaults_kwdict;
    PyObject *(*defaults_getter)(PyObject *);
    PyObject *func_annotations;
    PyObject *func_is_coroutine;
} __pyx_CyFunctionObject;
#undef __Pyx_CyOrPyCFunction_Check
#define __Pyx_CyFunction_Check(obj)  __Pyx_TypeCheck(obj, __pyx_CyFunctionType)
#define __Pyx_CyOrPyCFunction_Check(obj)  __Pyx_TypeCheck2(obj, __pyx_CyFunctionType, &PyCFunction_Type)
#define __Pyx_CyFunction_CheckExact(obj)  __Pyx_IS_TYPE(obj, __pyx_CyFunctionType)
static CYTHON_INLINE int __Pyx__IsSameCyOrCFunction(PyObject *func, void *cfunc);
#undef __Pyx_IsSameCFunction
#define __Pyx_IsSameCFunction(func, cfunc)   __Pyx__IsSameCyOrCFunction(func, cfunc)
static PyObject *__Pyx_CyFunction_Init(__pyx_CyFunctionObject* op, PyMethodDef *ml,
                                      int flags, PyObject* qualname,
                                      PyObject *closure,
                                      PyObject *module, PyObject *globals,
                                      PyObject* code);
static CYTHON_INLINE void __Pyx__CyFunction_SetClassObj(__pyx_CyFunctionObject* f, PyObject* classobj);
static CYTHON_INLINE void *__Pyx_CyFunction_InitDefaults(PyObject *m,
                                                         size_t size,
                                                         int pyobjects);
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsTuple(PyObject *m,
                                                            PyObject *tuple);
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsKwDict(PyObject *m,
                                                             PyObject *dict);
static CYTHON_INLINE void __Pyx_CyFunction_SetAnnotationsDict(PyObject *m,
                                                              PyObject *dict);
static int __pyx_CyFunction_init(PyObject *module);
#if CYTHON_METH_FASTCALL
static PyObject * __Pyx_CyFunction_Vectorcall_NOARGS(PyObject *func, PyObject *const *args, size_t nargsf, PyObject *kwnames);
static PyObject * __Pyx_CyFunction_Vectorcall_O(PyObject *func, PyObject *const *args, size_t nargsf, PyObject *kwnames);
static PyObject * __Pyx_CyFunction_Vectorcall_FASTCALL_KEYWORDS(PyObject *func, PyObject *const *args, size_t nargsf, PyObject *kwnames);
static PyObject * __Pyx_CyFunction_Vectorcall_FASTCALL_KEYWORDS_METHOD(PyObject *func, PyObject *const *args, size_t nargsf, PyObject *kwnames);
#if CYTHON_BACKPORT_VECTORCALL
#define __Pyx_CyFunction_func_vectorcall(f) (((__pyx_CyFunctionObject*)f)->func_vectorcall)
#else
#define __Pyx_CyFunction_func_vectorcall(f) (((PyCFunctionObject*)f)->vectorcall)
#endif
#endif


static PyObject *__Pyx_CyFunction_New(PyMethodDef *ml,
                                      int flags, PyObject* qualname,
                                      PyObject *closure,
                                      PyObject *module, PyObject *globals,
                                      PyObject* code);


static CYTHON_INLINE PyObject* __Pyx_PyObject_Call2Args(PyObject* function, PyObject* arg1, PyObject* arg2);


static CYTHON_INLINE PyObject* __Pyx_PyObject_CallOneArg(PyObject *func, PyObject *arg);


static int __Pyx_PyObject_GetMethod(PyObject *obj, PyObject *name, PyObject **method);


static PyObject* __Pyx_PyObject_CallMethod1(PyObject* obj, PyObject* method_name, PyObject* arg);


#if PY_MAJOR_VERSION < 3
#define __Pyx_PyString_Join __Pyx_PyBytes_Join
#define __Pyx_PyBaseString_Join(s, v) (PyUnicode_CheckExact(s) ? PyUnicode_Join(s, v) : __Pyx_PyBytes_Join(s, v))
#else
#define __Pyx_PyString_Join PyUnicode_Join
#define __Pyx_PyBaseString_Join PyUnicode_Join
#endif
static CYTHON_INLINE PyObject* __Pyx_PyBytes_Join(PyObject* sep, PyObject* values);


#if PY_MAJOR_VERSION >= 3
#define __Pyx_PyString_Equals __Pyx_PyUnicode_Equals
#else
#define __Pyx_PyString_Equals __Pyx_PyBytes_Equals
#endif


#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static CYTHON_INLINE int __Pyx_ListComp_Append(PyObject* list, PyObject* x) {
    PyListObject* L = (PyListObject*) list;
    Py_ssize_t len = Py_SIZE(list);
    if (likely(L->allocated > len)) {
        Py_INCREF(x);
        #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000
        L->ob_item[len] = x;
        #else
        PyList_SET_ITEM(list, len, x);
        #endif
        __Pyx_SET_SIZE(list, len + 1);
        return 0;
    }
    return PyList_Append(list, x);
}
#else
#define __Pyx_ListComp_Append(L,x) PyList_Append(L,x)
#endif


#if !CYTHON_COMPILING_IN_PYPY
static PyObject* __Pyx_PyInt_SubtractCObj(PyObject *op1, PyObject *op2, long intval, int inplace, int zerodivision_check);
#else
#define __Pyx_PyInt_SubtractCObj(op1, op2, intval, inplace, zerodivision_check)\
    (inplace ? PyNumber_InPlaceSubtract(op1, op2) : PyNumber_Subtract(op1, op2))
#endif


typedef struct {
    PyObject *type;
    PyObject **method_name;
    PyCFunction func;
    PyObject *method;
    int flag;
} __Pyx_CachedCFunction;


static PyObject* __Pyx__CallUnboundCMethod1(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg);
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_CallUnboundCMethod1(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg);
#else
#define __Pyx_CallUnboundCMethod1(cfunc, self, arg)  __Pyx__CallUnboundCMethod1(cfunc, self, arg)
#endif


#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY
static PyObject *__Pyx_PyDict_GetItem(PyObject *d, PyObject* key);
#define __Pyx_PyObject_Dict_GetItem(obj, name)\
    (likely(PyDict_CheckExact(obj)) ?\
     __Pyx_PyDict_GetItem(obj, name) : PyObject_GetItem(obj, name))
#else
#define __Pyx_PyDict_GetItem(d, key) PyObject_GetItem(d, key)
#define __Pyx_PyObject_Dict_GetItem(obj, name)  PyObject_GetItem(obj, name)
#endif


#if !CYTHON_COMPILING_IN_PYPY
static PyObject* __Pyx_PyInt_AddObjC(PyObject *op1, PyObject *op2, long intval, int inplace, int zerodivision_check);
#else
#define __Pyx_PyInt_AddObjC(op1, op2, intval, inplace, zerodivision_check)\
    (inplace ? PyNumber_InPlaceAdd(op1, op2) : PyNumber_Add(op1, op2))
#endif


# if CYTHON_COMPILING_IN_CPYTHON && PY_MAJOR_VERSION >= 3
    #if CYTHON_REFNANNY
        #define __Pyx_PyUnicode_ConcatInPlace(left, right) __Pyx_PyUnicode_ConcatInPlaceImpl(&left, right, __pyx_refnanny)
    #else
        #define __Pyx_PyUnicode_ConcatInPlace(left, right) __Pyx_PyUnicode_ConcatInPlaceImpl(&left, right)
    #endif
    static CYTHON_INLINE PyObject *__Pyx_PyUnicode_ConcatInPlaceImpl(PyObject **p_left, PyObject *right
        #if CYTHON_REFNANNY
        , void* __pyx_refnanny
        #endif
    );
#else
#define __Pyx_PyUnicode_ConcatInPlace __Pyx_PyUnicode_Concat
#endif
#define __Pyx_PyUnicode_ConcatInPlaceSafe(left, right) ((unlikely((left) == Py_None) || unlikely((right) == Py_None)) ?\
    PyNumber_InPlaceAdd(left, right) : __Pyx_PyUnicode_ConcatInPlace(left, right))


#if PY_MAJOR_VERSION >= 3
    #define __Pyx_PyStr_Concat __Pyx_PyUnicode_Concat
    #define __Pyx_PyStr_ConcatInPlace __Pyx_PyUnicode_ConcatInPlace
#else
    #define __Pyx_PyStr_Concat PyNumber_Add
    #define __Pyx_PyStr_ConcatInPlace PyNumber_InPlaceAdd
#endif
#define __Pyx_PyStr_ConcatSafe(a, b) ((unlikely((a) == Py_None) || unlikely((b) == Py_None)) ?\
    PyNumber_Add(a, b) : __Pyx_PyStr_Concat(a, b))
#define __Pyx_PyStr_ConcatInPlaceSafe(a, b) ((unlikely((a) == Py_None) || unlikely((b) == Py_None)) ?\
    PyNumber_InPlaceAdd(a, b) : __Pyx_PyStr_ConcatInPlace(a, b))


static CYTHON_INLINE int __Pyx_PyInt_BoolEqObjC(PyObject *op1, PyObject *op2, long intval, long inplace);


#if !CYTHON_COMPILING_IN_PYPY
static PyObject* __Pyx_PyInt_TrueDivideObjC(PyObject *op1, PyObject *op2, long intval, int inplace, int zerodivision_check);
#else
#define __Pyx_PyInt_TrueDivideObjC(op1, op2, intval, inplace, zerodivision_check)\
    (inplace ? PyNumber_InPlaceTrueDivide(op1, op2) : PyNumber_TrueDivide(op1, op2))
#endif


#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static CYTHON_INLINE int __Pyx_PyList_Append(PyObject* list, PyObject* x) {
    PyListObject* L = (PyListObject*) list;
    Py_ssize_t len = Py_SIZE(list);
    if (likely(L->allocated > len) & likely(len > (L->allocated >> 1))) {
        Py_INCREF(x);
        #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000
        L->ob_item[len] = x;
        #else
        PyList_SET_ITEM(list, len, x);
        #endif
        __Pyx_SET_SIZE(list, len + 1);
        return 0;
    }
    return PyList_Append(list, x);
}
#else
#define __Pyx_PyList_Append(L,x) PyList_Append(L,x)
#endif


#define __Pyx_GetItemInt(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck)\
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ?\
    __Pyx_GetItemInt_Fast(o, (Py_ssize_t)i, is_list, wraparound, boundscheck) :\
    (is_list ? (PyErr_SetString(PyExc_IndexError, "list index out of range"), (PyObject*)NULL) :\
               __Pyx_GetItemInt_Generic(o, to_py_func(i))))
#define __Pyx_GetItemInt_List(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck)\
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ?\
    __Pyx_GetItemInt_List_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) :\
    (PyErr_SetString(PyExc_IndexError, "list index out of range"), (PyObject*)NULL))
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck);
#define __Pyx_GetItemInt_Tuple(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck)\
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ?\
    __Pyx_GetItemInt_Tuple_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) :\
    (PyErr_SetString(PyExc_IndexError, "tuple index out of range"), (PyObject*)NULL))
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Tuple_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck);
static PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j);
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i,
                                                     int is_list, int wraparound, int boundscheck);


static double __Pyx_SlowPyString_AsDouble(PyObject *obj);
static double __Pyx__PyBytes_AsDouble(PyObject *obj, const char* start, Py_ssize_t length);
static CYTHON_INLINE double __Pyx_PyBytes_AsDouble(PyObject *obj) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS
    as_c_string = PyBytes_AS_STRING(obj);
    size = PyBytes_GET_SIZE(obj);
#else
    if (PyBytes_AsStringAndSize(obj, &as_c_string, &size) < 0) {
        return (double)-1;
    }
#endif
    return __Pyx__PyBytes_AsDouble(obj, as_c_string, size);
}
static CYTHON_INLINE double __Pyx_PyByteArray_AsDouble(PyObject *obj) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS
    as_c_string = PyByteArray_AS_STRING(obj);
    size = PyByteArray_GET_SIZE(obj);
#else
    as_c_string = PyByteArray_AsString(obj);
    if (as_c_string == NULL) {
        return (double)-1;
    }
    size = PyByteArray_Size(obj);
#endif
    return __Pyx__PyBytes_AsDouble(obj, as_c_string, size);
}


#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY && CYTHON_ASSUME_SAFE_MACROS
static const char* __Pyx__PyUnicode_AsDouble_Copy(const void* data, const int kind, char* buffer, Py_ssize_t start, Py_ssize_t end) {
    int last_was_punctuation;
    Py_ssize_t i;
    last_was_punctuation = 1;
    for (i=start; i <= end; i++) {
        Py_UCS4 chr = PyUnicode_READ(kind, data, i);
        int is_punctuation = (chr == '_') | (chr == '.');
        *buffer = (char)chr;
        buffer += (chr != '_');
        if (unlikely(chr > 127)) goto parse_failure;
        if (unlikely(last_was_punctuation & is_punctuation)) goto parse_failure;
        last_was_punctuation = is_punctuation;
    }
    if (unlikely(last_was_punctuation)) goto parse_failure;
    *buffer = '\0';
    return buffer;
parse_failure:
    return NULL;
}
static double __Pyx__PyUnicode_AsDouble_inf_nan(const void* data, int kind, Py_ssize_t start, Py_ssize_t length) {
    int matches = 1;
    Py_UCS4 chr;
    Py_UCS4 sign = PyUnicode_READ(kind, data, start);
    int is_signed = (sign == '-') | (sign == '+');
    start += is_signed;
    length -= is_signed;
    switch (PyUnicode_READ(kind, data, start)) {
        #ifdef Py_NAN
        case 'n':
        case 'N':
            if (unlikely(length != 3)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+1);
            matches &= (chr == 'a') | (chr == 'A');
            chr = PyUnicode_READ(kind, data, start+2);
            matches &= (chr == 'n') | (chr == 'N');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_NAN : Py_NAN;
        #endif
        case 'i':
        case 'I':
            if (unlikely(length < 3)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+1);
            matches &= (chr == 'n') | (chr == 'N');
            chr = PyUnicode_READ(kind, data, start+2);
            matches &= (chr == 'f') | (chr == 'F');
            if (likely(length == 3 && matches))
                return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
            if (unlikely(length != 8)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+3);
            matches &= (chr == 'i') | (chr == 'I');
            chr = PyUnicode_READ(kind, data, start+4);
            matches &= (chr == 'n') | (chr == 'N');
            chr = PyUnicode_READ(kind, data, start+5);
            matches &= (chr == 'i') | (chr == 'I');
            chr = PyUnicode_READ(kind, data, start+6);
            matches &= (chr == 't') | (chr == 'T');
            chr = PyUnicode_READ(kind, data, start+7);
            matches &= (chr == 'y') | (chr == 'Y');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
        case '.': case '0': case '1': case '2': case '3': case '4': case '5': case '6': case '7': case '8': case '9':
            break;
        default:
            goto parse_failure;
    }
    return 0.0;
parse_failure:
    return -1.0;
}
static double __Pyx_PyUnicode_AsDouble_WithSpaces(PyObject *obj) {
    double value;
    const char *last;
    char *end;
    Py_ssize_t start, length = PyUnicode_GET_LENGTH(obj);
    const int kind = PyUnicode_KIND(obj);
    const void* data = PyUnicode_DATA(obj);
    start = 0;
    while (Py_UNICODE_ISSPACE(PyUnicode_READ(kind, data, start)))
        start++;
    while (start < length - 1 && Py_UNICODE_ISSPACE(PyUnicode_READ(kind, data, length - 1)))
        length--;
    length -= start;
    if (unlikely(length <= 0)) goto fallback;
    value = __Pyx__PyUnicode_AsDouble_inf_nan(data, kind, start, length);
    if (unlikely(value == -1.0)) goto fallback;
    if (value != 0.0) return value;
    if (length < 40) {
        char number[40];
        last = __Pyx__PyUnicode_AsDouble_Copy(data, kind, number, start, start + length);
        if (unlikely(!last)) goto fallback;
        value = PyOS_string_to_double(number, &end, NULL);
    } else {
        char *number = (char*) PyMem_Malloc((length + 1) * sizeof(char));
        if (unlikely(!number)) goto fallback;
        last = __Pyx__PyUnicode_AsDouble_Copy(data, kind, number, start, start + length);
        if (unlikely(!last)) {
            PyMem_Free(number);
            goto fallback;
        }
        value = PyOS_string_to_double(number, &end, NULL);
        PyMem_Free(number);
    }
    if (likely(end == last) || (value == (double)-1 && PyErr_Occurred())) {
        return value;
    }
fallback:
    return __Pyx_SlowPyString_AsDouble(obj);
}
#endif
static CYTHON_INLINE double __Pyx_PyUnicode_AsDouble(PyObject *obj) {
#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY && CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(__Pyx_PyUnicode_READY(obj) == -1))
        return (double)-1;
    if (likely(PyUnicode_IS_ASCII(obj))) {
        const char *s;
        Py_ssize_t length;
        s = PyUnicode_AsUTF8AndSize(obj, &length);
        return __Pyx__PyBytes_AsDouble(obj, s, length);
    }
    return __Pyx_PyUnicode_AsDouble_WithSpaces(obj);
#else
    return __Pyx_SlowPyString_AsDouble(obj);
#endif
}


static CYTHON_INLINE double __Pyx_PyString_AsDouble(PyObject *obj) {
    #if PY_MAJOR_VERSION >= 3
    (void)__Pyx_PyBytes_AsDouble;
    return __Pyx_PyUnicode_AsDouble(obj);
    #else
    (void)__Pyx_PyUnicode_AsDouble;
    return __Pyx_PyBytes_AsDouble(obj);
    #endif
}


#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyList_GetSlice(PyObject* src, Py_ssize_t start, Py_ssize_t stop);
static CYTHON_INLINE PyObject* __Pyx_PyTuple_GetSlice(PyObject* src, Py_ssize_t start, Py_ssize_t stop);
#else
#define __Pyx_PyList_GetSlice(seq, start, stop)   PySequence_GetSlice(seq, start, stop)
#define __Pyx_PyTuple_GetSlice(seq, start, stop)  PySequence_GetSlice(seq, start, stop)
#endif


static CYTHON_INLINE void __Pyx_RaiseUnboundLocalError(const char *varname);


static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list, int level);


static PyObject* __Pyx_ImportFrom(PyObject* module, PyObject* name);


#if CYTHON_USE_TYPE_SLOTS
static CYTHON_INLINE PyObject *__Pyx_PyObject_GetItem(PyObject *obj, PyObject *key);
#else
#define __Pyx_PyObject_GetItem(obj, key)  PyObject_GetItem(obj, key)
#endif


static CYTHON_INLINE PyObject* __Pyx_PyObject_CallNoArg(PyObject *func);


static PyObject* __Pyx_PyObject_CallMethod0(PyObject* obj, PyObject* method_name);


#if CYTHON_COMPILING_IN_CPYTHON || CYTHON_COMPILING_IN_LIMITED_API || CYTHON_USE_TYPE_SPECS
static int __Pyx_validate_bases_tuple(const char *type_name, Py_ssize_t dictoffset, PyObject *bases);
#endif


CYTHON_UNUSED static int __Pyx_PyType_Ready(PyTypeObject *t);


#if CYTHON_USE_TYPE_SLOTS && CYTHON_USE_PYTYPE_LOOKUP && PY_VERSION_HEX < 0x03070000
static CYTHON_INLINE PyObject* __Pyx_PyObject_GenericGetAttrNoDict(PyObject* obj, PyObject* attr_name);
#else
#define __Pyx_PyObject_GenericGetAttrNoDict PyObject_GenericGetAttr
#endif


static PyObject *__Pyx_ImportDottedModule(PyObject *name, PyObject *parts_tuple);
#if PY_MAJOR_VERSION >= 3
static PyObject *__Pyx_ImportDottedModule_WalkParts(PyObject *module, PyObject *name, PyObject *parts_tuple);
#endif


#ifdef CYTHON_CLINE_IN_TRACEBACK
#define __Pyx_CLineForTraceback(tstate, c_line)  (((CYTHON_CLINE_IN_TRACEBACK)) ? c_line : 0)
#else
static int __Pyx_CLineForTraceback(PyThreadState *tstate, int c_line);
#endif


#if !CYTHON_COMPILING_IN_LIMITED_API
typedef struct {
    PyCodeObject* code_object;
    int code_line;
} __Pyx_CodeObjectCacheEntry;
struct __Pyx_CodeObjectCache {
    int count;
    int max_count;
    __Pyx_CodeObjectCacheEntry* entries;
};
static struct __Pyx_CodeObjectCache __pyx_code_cache = {0,0,NULL};
static int __pyx_bisect_code_objects(__Pyx_CodeObjectCacheEntry* entries, int count, int code_line);
static PyCodeObject *__pyx_find_code_object(int code_line);
static void __pyx_insert_code_object(int code_line, PyCodeObject* code_object);
#endif


static void __Pyx_AddTraceback(const char *funcname, int c_line,
                               int py_line, const char *filename);


#if !defined(__INTEL_COMPILER) && defined(__GNUC__) && (__GNUC__ > 4 || (__GNUC__ == 4 && __GNUC_MINOR__ >= 6))
#define __Pyx_HAS_GCC_DIAGNOSTIC
#endif


static CYTHON_INLINE PyObject* __Pyx_PyInt_From_long(long value);


#if CYTHON_COMPILING_IN_LIMITED_API
typedef PyObject *__Pyx_TypeName;
#define __Pyx_FMT_TYPENAME "%U"
static __Pyx_TypeName __Pyx_PyType_GetName(PyTypeObject* tp);
#define __Pyx_DECREF_TypeName(obj) Py_XDECREF(obj)
#else
typedef const char *__Pyx_TypeName;
#define __Pyx_FMT_TYPENAME "%.200s"
#define __Pyx_PyType_GetName(tp) ((tp)->tp_name)
#define __Pyx_DECREF_TypeName(obj)
#endif


static CYTHON_INLINE long __Pyx_PyInt_As_long(PyObject *);


static CYTHON_INLINE int __Pyx_PyInt_As_int(PyObject *);


#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_TypeCheck(obj, type) __Pyx_IsSubtype(Py_TYPE(obj), (PyTypeObject *)type)
#define __Pyx_TypeCheck2(obj, type1, type2) __Pyx_IsAnySubtype2(Py_TYPE(obj), (PyTypeObject *)type1, (PyTypeObject *)type2)
static CYTHON_INLINE int __Pyx_IsSubtype(PyTypeObject *a, PyTypeObject *b);
static CYTHON_INLINE int __Pyx_IsAnySubtype2(PyTypeObject *cls, PyTypeObject *a, PyTypeObject *b);
static CYTHON_INLINE int __Pyx_PyErr_GivenExceptionMatches(PyObject *err, PyObject *type);
static CYTHON_INLINE int __Pyx_PyErr_GivenExceptionMatches2(PyObject *err, PyObject *type1, PyObject *type2);
#else
#define __Pyx_TypeCheck(obj, type) PyObject_TypeCheck(obj, (PyTypeObject *)type)
#define __Pyx_TypeCheck2(obj, type1, type2) (PyObject_TypeCheck(obj, (PyTypeObject *)type1) || PyObject_TypeCheck(obj, (PyTypeObject *)type2))
#define __Pyx_PyErr_GivenExceptionMatches(err, type) PyErr_GivenExceptionMatches(err, type)
#define __Pyx_PyErr_GivenExceptionMatches2(err, type1, type2) (PyErr_GivenExceptionMatches(err, type1) || PyErr_GivenExceptionMatches(err, type2))
#endif
#define __Pyx_PyErr_ExceptionMatches2(err1, err2)  __Pyx_PyErr_GivenExceptionMatches2(__Pyx_PyErr_CurrentExceptionType(), err1, err2)
#define __Pyx_PyException_Check(obj) __Pyx_TypeCheck(obj, PyExc_Exception)


static unsigned long __Pyx_get_runtime_version(void);
static int __Pyx_check_binary_version(unsigned long ct_version, unsigned long rt_version, int allow_newer);


static int __Pyx_InitStrings(__Pyx_StringTabEntry *t);






#define __Pyx_MODULE_NAME "qutk"
extern int __pyx_module_is_main_qutk;
int __pyx_module_is_main_qutk = 0;



static PyObject *__pyx_builtin_sum;
static PyObject *__pyx_builtin_range;
static PyObject *__pyx_builtin_zip;
static PyObject *__pyx_builtin_max;

static const char __pyx_k_[] = "\316\273";
static const char __pyx_k_A[] = "A";
static const char __pyx_k_P[] = "P";
static const char __pyx_k_Q[] = "Q";
static const char __pyx_k_d[] = "d";
static const char __pyx_k_e[] = "\316\273e";
static const char __pyx_k_i[] = "i";
static const char __pyx_k_k[] = "k";
static const char __pyx_k_n[] = "n";
static const char __pyx_k_s[] = "s";
static const char __pyx_k_t[] = "t";
static const char __pyx_k_z[] = "z";
static const char __pyx_k_Lq[] = "Lq";
static const char __pyx_k_Ls[] = "Ls";
static const char __pyx_k_P0[] = "P0";
static const char __pyx_k_Wq[] = "Wq";
static const char __pyx_k_Ws[] = "Ws";
static const char __pyx_k__2[] = "\316\274";
static const char __pyx_k__3[] = "/";
static const char __pyx_k__8[] = "\317\201";
static const char __pyx_k__9[] = " ";
static const char __pyx_k_gc[] = "gc";
static const char __pyx_k_P_i[] = "P%i";
static const char __pyx_k__10[] = "\342\210\236";
static const char __pyx_k__11[] = "\316\267";
static const char __pyx_k__12[] = ".";
static const char __pyx_k__13[] = "*";
static const char __pyx_k__14[] = "_";
static const char __pyx_k__24[] = "?";
static const char __pyx_k_exp[] = "exp";
static const char __pyx_k_inf[] = "inf";
static const char __pyx_k_max[] = "max";
static const char __pyx_k_miu[] = "miu";
static const char __pyx_k_s_2[] = "_s";
static const char __pyx_k_s_3[] = "s_";
static const char __pyx_k_sum[] = "sum";
static const char __pyx_k_zip[] = "zip";
static const char __pyx_k_best[] = "best";
static const char __pyx_k_ceil[] = "ceil";
static const char __pyx_k_cost[] = "cost";
static const char __pyx_k_join[] = "join";
static const char __pyx_k_main[] = "__main__";
static const char __pyx_k_math[] = "math";
static const char __pyx_k_name[] = "__name__";
static const char __pyx_k_qutk[] = "qutk";
static const char __pyx_k_spec[] = "__spec__";
static const char __pyx_k_test[] = "__test__";
static const char __pyx_k_M_M_1[] = "M/M/1/\342\210\236";
static const char __pyx_k_M_M_i[] = "M/M/%i/\342\210\236";
static const char __pyx_k_P_N_i[] = "P{N>%i}";
static const char __pyx_k_P_T_f[] = "P{T>%f}";
static const char __pyx_k_Plost[] = "Plost";
static const char __pyx_k_index[] = "index";
static const char __pyx_k_model[] = "model";
static const char __pyx_k_range[] = "range";
static const char __pyx_k_split[] = "split";
static const char __pyx_k_detail[] = "detail";
static const char __pyx_k_enable[] = "enable";
static const char __pyx_k_fsolve[] = "fsolve";
static const char __pyx_k_import[] = "__import__";
static const char __pyx_k_method[] = "method";
static const char __pyx_k_remark[] = "remark";
static const char __pyx_k_update[] = "update";
static const char __pyx_k_disable[] = "disable";
static const char __pyx_k_indices[] = "indices";
static const char __pyx_k_qutk_py[] = "qutk.py";
static const char __pyx_k_max_wait[] = "max_wait";
static const char __pyx_k_min_cost[] = "min_cost";
static const char __pyx_k_n_server[] = "n_server";
static const char __pyx_k_factorial[] = "factorial";
static const char __pyx_k_isenabled[] = "isenabled";
static const char __pyx_k_max_queue[] = "max_queue";
static const char __pyx_k_wait_cost[] = "wait_cost";
static const char __pyx_k_t_wait_max[] = "t_wait_max";
static const char __pyx_k_n_queue_max[] = "n_queue_max";
static const char __pyx_k_server_cost[] = "server_cost";
static const char __pyx_k_initializing[] = "_initializing";
static const char __pyx_k_is_coroutine[] = "_is_coroutine";
static const char __pyx_k_n_server_max[] = "n_server_max";
static const char __pyx_k_class_getitem[] = "__class_getitem__";
static const char __pyx_k_return_detail[] = "return_detail";
static const char __pyx_k_server_income[] = "server_income";
static const char __pyx_k_index_locals_P[] = "index.<locals>.P";
static const char __pyx_k_scipy_optimize[] = "scipy.optimize";
static const char __pyx_k_miu_locals_lambda[] = "miu.<locals>.<lambda>";
static const char __pyx_k_server_efficiency[] = "\316\267: server efficiency.";
static const char __pyx_k_asyncio_coroutines[] = "asyncio.coroutines";
static const char __pyx_k_cline_in_traceback[] = "cline_in_traceback";
static const char __pyx_k_A_absolute_passability[] = "A: absolute passability.";
static const char __pyx_k_Q_relative_passability[] = "Q: relative passability.";
static const char __pyx_k_Wq_average_waiting_time[] = "Wq: average waiting time.";
static const char __pyx_k_Created_on_Thu_Dec_14_14_54_55[] = "\nCreated on Thu Dec 14 14:54:55 2023\n\n@author: ThinkPad\n";
static const char __pyx_k_Lq_average_waiting_queue_length[] = "Lq: average waiting queue length, the number of customers waiting in the system.";
static const char __pyx_k_Plost_the_probability_of_system[] = "Plost: the probability of system loss some customers.";
static const char __pyx_k_Ws_average_staying_time_average[] = "Ws: average staying time, average busy time.";
static const char __pyx_k_average_service_rate_per_server[] = "\316\274: average service rate per server, the number of customers processed by each server per unit time.";
static const char __pyx_k_service_intensity_the_probabili[] = "\317\201: service intensity, the probability of at least one customer in the system, the probability of the system being busy.";
static const char __pyx_k_system_average_arrival_rate_the[] = "\316\273: system average arrival rate, the number of customers arriving per unit time.";
static const char __pyx_k_Ls_average_queue_length_the_aver[] = "Ls: average queue length, the average number of customers in the system.";
static const char __pyx_k_P0_the_probability_of_system_idl[] = "P0: the probability of system idle, the probability of no customer in the system, the probability of not queuing.";
static const char __pyx_k_P_N_i_the_probability_of_more_th[] = "P{N>%i}: the probability of more than %i customers in the system.";
static const char __pyx_k_P_T_g_the_probability_of_staying[] = "P{T>%g}: the probability of staying in the system for more than %g.";
static const char __pyx_k_P_i_the_probability_of_i_in_cust[] = "P%i: the probability of %i in customers in the system.";
static const char __pyx_k_e_system_average_effective_arriv[] = "\316\273e: system average effective arrival rate, the number of customers effective arriving per unit time.Ws: average staying time, average busy time.";

static PyObject *__pyx_pf_4qutk_5index_P(PyObject *__pyx_self, PyObject *__pyx_v_n, PyObject *__pyx_v_s, PyObject *__pyx_v_k); 
static PyObject *__pyx_pf_4qutk_index(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_Uv__5cg, PyObject *__pyx_Uv__fdg, PyObject *__pyx_v_n, PyObject *__pyx_v_t, PyObject *__pyx_v_model); 
static PyObject *__pyx_pf_4qutk_2n_server(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_Uv__5cg, PyObject *__pyx_Uv__fdg, PyObject *__pyx_v_server_cost, PyObject *__pyx_v_wait_cost, PyObject *__pyx_v_n_server_max, PyObject *__pyx_v_n_queue_max, PyObject *__pyx_v_t_wait_max, PyObject *__pyx_v_method, PyObject *__pyx_v_return_detail); 
static PyObject *__pyx_lambda_funcdef_lambda(PyObject *__pyx_self, PyObject *__pyx_Uv__fdg); 
static PyObject *__pyx_pf_4qutk_4miu(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_Uv__5cg, PyObject *__pyx_v_k, PyObject *__pyx_v_server_cost, PyObject *__pyx_v_wait_cost, PyObject *__pyx_v_server_income); 
static PyObject *__pyx_tp_new_4qutk___pyx_scope_struct__index(PyTypeObject *t, PyObject *a, PyObject *k); 
static PyObject *__pyx_tp_new_4qutk___pyx_scope_struct_1_miu(PyTypeObject *t, PyObject *a, PyObject *k); 
static __Pyx_CachedCFunction __pyx_umethod_PyDict_Type_update = {0, 0, 0, 0, 0};
static __Pyx_CachedCFunction __pyx_umethod_PyList_Type_index = {0, 0, 0, 0, 0};


typedef struct {
  PyObject *__pyx_d;
  PyObject *__pyx_b;
  PyObject *__pyx_cython_runtime;
  PyObject *__pyx_empty_tuple;
  PyObject *__pyx_empty_bytes;
  PyObject *__pyx_empty_unicode;
  #ifdef __Pyx_CyFunction_USED
  PyTypeObject *__pyx_CyFunctionType;
  #endif
  #ifdef __Pyx_FusedFunction_USED
  PyTypeObject *__pyx_FusedFunctionType;
  #endif
  #ifdef __Pyx_Generator_USED
  PyTypeObject *__pyx_GeneratorType;
  #endif
  #ifdef __Pyx_IterableCoroutine_USED
  PyTypeObject *__pyx_IterableCoroutineType;
  #endif
  #ifdef __Pyx_Coroutine_USED
  PyTypeObject *__pyx_CoroutineAwaitType;
  #endif
  #ifdef __Pyx_Coroutine_USED
  PyTypeObject *__pyx_CoroutineType;
  #endif
  #if CYTHON_USE_MODULE_STATE
  PyObject *__pyx_type_4qutk___pyx_scope_struct__index;
  PyObject *__pyx_type_4qutk___pyx_scope_struct_1_miu;
  #endif
  PyTypeObject *__pyx_ptype_4qutk___pyx_scope_struct__index;
  PyTypeObject *__pyx_ptype_4qutk___pyx_scope_struct_1_miu;
  PyObject *__pyx_n_s_;
  PyObject *__pyx_n_s_A;
  PyObject *__pyx_kp_s_A_absolute_passability;
  PyObject *__pyx_n_s_Lq;
  PyObject *__pyx_kp_s_Lq_average_waiting_queue_length;
  PyObject *__pyx_n_s_Ls;
  PyObject *__pyx_kp_s_Ls_average_queue_length_the_aver;
  PyObject *__pyx_kp_s_M_M_1;
  PyObject *__pyx_kp_s_M_M_i;
  PyObject *__pyx_n_s_P;
  PyObject *__pyx_n_s_P0;
  PyObject *__pyx_kp_s_P0_the_probability_of_system_idl;
  PyObject *__pyx_kp_s_P_N_i;
  PyObject *__pyx_kp_s_P_N_i_the_probability_of_more_th;
  PyObject *__pyx_kp_s_P_T_f;
  PyObject *__pyx_kp_s_P_T_g_the_probability_of_staying;
  PyObject *__pyx_kp_s_P_i;
  PyObject *__pyx_kp_s_P_i_the_probability_of_i_in_cust;
  PyObject *__pyx_n_s_Plost;
  PyObject *__pyx_kp_s_Plost_the_probability_of_system;
  PyObject *__pyx_n_s_Q;
  PyObject *__pyx_kp_s_Q_relative_passability;
  PyObject *__pyx_n_s_Wq;
  PyObject *__pyx_kp_s_Wq_average_waiting_time;
  PyObject *__pyx_n_s_Ws;
  PyObject *__pyx_kp_s_Ws_average_staying_time_average;
  PyObject *__pyx_kp_s__10;
  PyObject *__pyx_kp_s__11;
  PyObject *__pyx_kp_u__12;
  PyObject *__pyx_n_s__13;
  PyObject *__pyx_n_s__14;
  PyObject *__pyx_n_s__2;
  PyObject *__pyx_n_s__24;
  PyObject *__pyx_kp_s__3;
  PyObject *__pyx_kp_s__8;
  PyObject *__pyx_kp_s__9;
  PyObject *__pyx_n_s_asyncio_coroutines;
  PyObject *__pyx_kp_s_average_service_rate_per_server;
  PyObject *__pyx_n_s_best;
  PyObject *__pyx_n_s_ceil;
  PyObject *__pyx_n_s_class_getitem;
  PyObject *__pyx_n_s_cline_in_traceback;
  PyObject *__pyx_n_s_cost;
  PyObject *__pyx_n_s_d;
  PyObject *__pyx_n_s_detail;
  PyObject *__pyx_kp_u_disable;
  PyObject *__pyx_kp_s_e;
  PyObject *__pyx_kp_s_e_system_average_effective_arriv;
  PyObject *__pyx_kp_u_enable;
  PyObject *__pyx_n_s_exp;
  PyObject *__pyx_n_s_factorial;
  PyObject *__pyx_n_s_fsolve;
  PyObject *__pyx_kp_u_gc;
  PyObject *__pyx_n_s_i;
  PyObject *__pyx_n_s_import;
  PyObject *__pyx_n_s_index;
  PyObject *__pyx_n_s_index_locals_P;
  PyObject *__pyx_n_s_indices;
  PyObject *__pyx_n_s_inf;
  PyObject *__pyx_n_s_initializing;
  PyObject *__pyx_n_s_is_coroutine;
  PyObject *__pyx_kp_u_isenabled;
  PyObject *__pyx_n_s_join;
  PyObject *__pyx_n_s_k;
  PyObject *__pyx_n_s_main;
  PyObject *__pyx_n_s_math;
  PyObject *__pyx_n_s_max;
  PyObject *__pyx_n_s_max_queue;
  PyObject *__pyx_n_s_max_wait;
  PyObject *__pyx_n_s_method;
  PyObject *__pyx_n_s_min_cost;
  PyObject *__pyx_n_s_miu;
  PyObject *__pyx_n_s_miu_locals_lambda;
  PyObject *__pyx_n_s_model;
  PyObject *__pyx_n_s_n;
  PyObject *__pyx_n_s_n_queue_max;
  PyObject *__pyx_n_s_n_server;
  PyObject *__pyx_n_s_n_server_max;
  PyObject *__pyx_n_s_name;
  PyObject *__pyx_n_s_qutk;
  PyObject *__pyx_kp_s_qutk_py;
  PyObject *__pyx_n_s_range;
  PyObject *__pyx_n_s_remark;
  PyObject *__pyx_n_s_return_detail;
  PyObject *__pyx_n_s_s;
  PyObject *__pyx_n_s_s_2;
  PyObject *__pyx_n_s_s_3;
  PyObject *__pyx_n_s_scipy_optimize;
  PyObject *__pyx_n_s_server_cost;
  PyObject *__pyx_kp_s_server_efficiency;
  PyObject *__pyx_n_s_server_income;
  PyObject *__pyx_kp_s_service_intensity_the_probabili;
  PyObject *__pyx_n_s_spec;
  PyObject *__pyx_n_s_split;
  PyObject *__pyx_n_s_sum;
  PyObject *__pyx_kp_s_system_average_arrival_rate_the;
  PyObject *__pyx_n_s_t;
  PyObject *__pyx_n_s_t_wait_max;
  PyObject *__pyx_n_s_test;
  PyObject *__pyx_n_s_update;
  PyObject *__pyx_n_s_wait_cost;
  PyObject *__pyx_n_s_z;
  PyObject *__pyx_n_s_zip;
  PyObject *__pyx_float_0_5;
  PyObject *__pyx_int_0;
  PyObject *__pyx_int_1;
  PyObject *__pyx_int_2;
  PyObject *__pyx_int_4;
  PyObject *__pyx_int_100;
  PyObject *__pyx_int_neg_1;
  PyObject *__pyx_slice__4;
  PyObject *__pyx_tuple__5;
  PyObject *__pyx_tuple__7;
  PyObject *__pyx_tuple__15;
  PyObject *__pyx_tuple__17;
  PyObject *__pyx_tuple__18;
  PyObject *__pyx_tuple__20;
  PyObject *__pyx_tuple__21;
  PyObject *__pyx_tuple__23;
  PyObject *__pyx_codeobj__6;
  PyObject *__pyx_codeobj__16;
  PyObject *__pyx_codeobj__19;
  PyObject *__pyx_codeobj__22;
} __pyx_mstate;

#if CYTHON_USE_MODULE_STATE
#ifdef __cplusplus
namespace {
  extern struct PyModuleDef __pyx_moduledef;
} 
#else
static struct PyModuleDef __pyx_moduledef;
#endif

#define __pyx_mstate(o) ((__pyx_mstate *)__Pyx_PyModule_GetState(o))

#define __pyx_mstate_global (__pyx_mstate(PyState_FindModule(&__pyx_moduledef)))

#define __pyx_m (PyState_FindModule(&__pyx_moduledef))
#else
static __pyx_mstate __pyx_mstate_global_static =
#ifdef __cplusplus
    {};
#else
    {0};
#endif
static __pyx_mstate *__pyx_mstate_global = &__pyx_mstate_global_static;
#endif

#if CYTHON_USE_MODULE_STATE
static int __pyx_m_clear(PyObject *m) {
  __pyx_mstate *clear_module_state = __pyx_mstate(m);
  if (!clear_module_state) return 0;
  Py_CLEAR(clear_module_state->__pyx_d);
  Py_CLEAR(clear_module_state->__pyx_b);
  Py_CLEAR(clear_module_state->__pyx_cython_runtime);
  Py_CLEAR(clear_module_state->__pyx_empty_tuple);
  Py_CLEAR(clear_module_state->__pyx_empty_bytes);
  Py_CLEAR(clear_module_state->__pyx_empty_unicode);
  #ifdef __Pyx_CyFunction_USED
  Py_CLEAR(clear_module_state->__pyx_CyFunctionType);
  #endif
  #ifdef __Pyx_FusedFunction_USED
  Py_CLEAR(clear_module_state->__pyx_FusedFunctionType);
  #endif
  Py_CLEAR(clear_module_state->__pyx_ptype_4qutk___pyx_scope_struct__index);
  Py_CLEAR(clear_module_state->__pyx_type_4qutk___pyx_scope_struct__index);
  Py_CLEAR(clear_module_state->__pyx_ptype_4qutk___pyx_scope_struct_1_miu);
  Py_CLEAR(clear_module_state->__pyx_type_4qutk___pyx_scope_struct_1_miu);
  Py_CLEAR(clear_module_state->__pyx_n_s_);
  Py_CLEAR(clear_module_state->__pyx_n_s_A);
  Py_CLEAR(clear_module_state->__pyx_kp_s_A_absolute_passability);
  Py_CLEAR(clear_module_state->__pyx_n_s_Lq);
  Py_CLEAR(clear_module_state->__pyx_kp_s_Lq_average_waiting_queue_length);
  Py_CLEAR(clear_module_state->__pyx_n_s_Ls);
  Py_CLEAR(clear_module_state->__pyx_kp_s_Ls_average_queue_length_the_aver);
  Py_CLEAR(clear_module_state->__pyx_kp_s_M_M_1);
  Py_CLEAR(clear_module_state->__pyx_kp_s_M_M_i);
  Py_CLEAR(clear_module_state->__pyx_n_s_P);
  Py_CLEAR(clear_module_state->__pyx_n_s_P0);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P0_the_probability_of_system_idl);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P_N_i);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P_N_i_the_probability_of_more_th);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P_T_f);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P_T_g_the_probability_of_staying);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P_i);
  Py_CLEAR(clear_module_state->__pyx_kp_s_P_i_the_probability_of_i_in_cust);
  Py_CLEAR(clear_module_state->__pyx_n_s_Plost);
  Py_CLEAR(clear_module_state->__pyx_kp_s_Plost_the_probability_of_system);
  Py_CLEAR(clear_module_state->__pyx_n_s_Q);
  Py_CLEAR(clear_module_state->__pyx_kp_s_Q_relative_passability);
  Py_CLEAR(clear_module_state->__pyx_n_s_Wq);
  Py_CLEAR(clear_module_state->__pyx_kp_s_Wq_average_waiting_time);
  Py_CLEAR(clear_module_state->__pyx_n_s_Ws);
  Py_CLEAR(clear_module_state->__pyx_kp_s_Ws_average_staying_time_average);
  Py_CLEAR(clear_module_state->__pyx_kp_s__10);
  Py_CLEAR(clear_module_state->__pyx_kp_s__11);
  Py_CLEAR(clear_module_state->__pyx_kp_u__12);
  Py_CLEAR(clear_module_state->__pyx_n_s__13);
  Py_CLEAR(clear_module_state->__pyx_n_s__14);
  Py_CLEAR(clear_module_state->__pyx_n_s__2);
  Py_CLEAR(clear_module_state->__pyx_n_s__24);
  Py_CLEAR(clear_module_state->__pyx_kp_s__3);
  Py_CLEAR(clear_module_state->__pyx_kp_s__8);
  Py_CLEAR(clear_module_state->__pyx_kp_s__9);
  Py_CLEAR(clear_module_state->__pyx_n_s_asyncio_coroutines);
  Py_CLEAR(clear_module_state->__pyx_kp_s_average_service_rate_per_server);
  Py_CLEAR(clear_module_state->__pyx_n_s_best);
  Py_CLEAR(clear_module_state->__pyx_n_s_ceil);
  Py_CLEAR(clear_module_state->__pyx_n_s_class_getitem);
  Py_CLEAR(clear_module_state->__pyx_n_s_cline_in_traceback);
  Py_CLEAR(clear_module_state->__pyx_n_s_cost);
  Py_CLEAR(clear_module_state->__pyx_n_s_d);
  Py_CLEAR(clear_module_state->__pyx_n_s_detail);
  Py_CLEAR(clear_module_state->__pyx_kp_u_disable);
  Py_CLEAR(clear_module_state->__pyx_kp_s_e);
  Py_CLEAR(clear_module_state->__pyx_kp_s_e_system_average_effective_arriv);
  Py_CLEAR(clear_module_state->__pyx_kp_u_enable);
  Py_CLEAR(clear_module_state->__pyx_n_s_exp);
  Py_CLEAR(clear_module_state->__pyx_n_s_factorial);
  Py_CLEAR(clear_module_state->__pyx_n_s_fsolve);
  Py_CLEAR(clear_module_state->__pyx_kp_u_gc);
  Py_CLEAR(clear_module_state->__pyx_n_s_i);
  Py_CLEAR(clear_module_state->__pyx_n_s_import);
  Py_CLEAR(clear_module_state->__pyx_n_s_index);
  Py_CLEAR(clear_module_state->__pyx_n_s_index_locals_P);
  Py_CLEAR(clear_module_state->__pyx_n_s_indices);
  Py_CLEAR(clear_module_state->__pyx_n_s_inf);
  Py_CLEAR(clear_module_state->__pyx_n_s_initializing);
  Py_CLEAR(clear_module_state->__pyx_n_s_is_coroutine);
  Py_CLEAR(clear_module_state->__pyx_kp_u_isenabled);
  Py_CLEAR(clear_module_state->__pyx_n_s_join);
  Py_CLEAR(clear_module_state->__pyx_n_s_k);
  Py_CLEAR(clear_module_state->__pyx_n_s_main);
  Py_CLEAR(clear_module_state->__pyx_n_s_math);
  Py_CLEAR(clear_module_state->__pyx_n_s_max);
  Py_CLEAR(clear_module_state->__pyx_n_s_max_queue);
  Py_CLEAR(clear_module_state->__pyx_n_s_max_wait);
  Py_CLEAR(clear_module_state->__pyx_n_s_method);
  Py_CLEAR(clear_module_state->__pyx_n_s_min_cost);
  Py_CLEAR(clear_module_state->__pyx_n_s_miu);
  Py_CLEAR(clear_module_state->__pyx_n_s_miu_locals_lambda);
  Py_CLEAR(clear_module_state->__pyx_n_s_model);
  Py_CLEAR(clear_module_state->__pyx_n_s_n);
  Py_CLEAR(clear_module_state->__pyx_n_s_n_queue_max);
  Py_CLEAR(clear_module_state->__pyx_n_s_n_server);
  Py_CLEAR(clear_module_state->__pyx_n_s_n_server_max);
  Py_CLEAR(clear_module_state->__pyx_n_s_name);
  Py_CLEAR(clear_module_state->__pyx_n_s_qutk);
  Py_CLEAR(clear_module_state->__pyx_kp_s_qutk_py);
  Py_CLEAR(clear_module_state->__pyx_n_s_range);
  Py_CLEAR(clear_module_state->__pyx_n_s_remark);
  Py_CLEAR(clear_module_state->__pyx_n_s_return_detail);
  Py_CLEAR(clear_module_state->__pyx_n_s_s);
  Py_CLEAR(clear_module_state->__pyx_n_s_s_2);
  Py_CLEAR(clear_module_state->__pyx_n_s_s_3);
  Py_CLEAR(clear_module_state->__pyx_n_s_scipy_optimize);
  Py_CLEAR(clear_module_state->__pyx_n_s_server_cost);
  Py_CLEAR(clear_module_state->__pyx_kp_s_server_efficiency);
  Py_CLEAR(clear_module_state->__pyx_n_s_server_income);
  Py_CLEAR(clear_module_state->__pyx_kp_s_service_intensity_the_probabili);
  Py_CLEAR(clear_module_state->__pyx_n_s_spec);
  Py_CLEAR(clear_module_state->__pyx_n_s_split);
  Py_CLEAR(clear_module_state->__pyx_n_s_sum);
  Py_CLEAR(clear_module_state->__pyx_kp_s_system_average_arrival_rate_the);
  Py_CLEAR(clear_module_state->__pyx_n_s_t);
  Py_CLEAR(clear_module_state->__pyx_n_s_t_wait_max);
  Py_CLEAR(clear_module_state->__pyx_n_s_test);
  Py_CLEAR(clear_module_state->__pyx_n_s_update);
  Py_CLEAR(clear_module_state->__pyx_n_s_wait_cost);
  Py_CLEAR(clear_module_state->__pyx_n_s_z);
  Py_CLEAR(clear_module_state->__pyx_n_s_zip);
  Py_CLEAR(clear_module_state->__pyx_float_0_5);
  Py_CLEAR(clear_module_state->__pyx_int_0);
  Py_CLEAR(clear_module_state->__pyx_int_1);
  Py_CLEAR(clear_module_state->__pyx_int_2);
  Py_CLEAR(clear_module_state->__pyx_int_4);
  Py_CLEAR(clear_module_state->__pyx_int_100);
  Py_CLEAR(clear_module_state->__pyx_int_neg_1);
  Py_CLEAR(clear_module_state->__pyx_slice__4);
  Py_CLEAR(clear_module_state->__pyx_tuple__5);
  Py_CLEAR(clear_module_state->__pyx_tuple__7);
  Py_CLEAR(clear_module_state->__pyx_tuple__15);
  Py_CLEAR(clear_module_state->__pyx_tuple__17);
  Py_CLEAR(clear_module_state->__pyx_tuple__18);
  Py_CLEAR(clear_module_state->__pyx_tuple__20);
  Py_CLEAR(clear_module_state->__pyx_tuple__21);
  Py_CLEAR(clear_module_state->__pyx_tuple__23);
  Py_CLEAR(clear_module_state->__pyx_codeobj__6);
  Py_CLEAR(clear_module_state->__pyx_codeobj__16);
  Py_CLEAR(clear_module_state->__pyx_codeobj__19);
  Py_CLEAR(clear_module_state->__pyx_codeobj__22);
  return 0;
}
#endif

#if CYTHON_USE_MODULE_STATE
static int __pyx_m_traverse(PyObject *m, visitproc visit, void *arg) {
  __pyx_mstate *traverse_module_state = __pyx_mstate(m);
  if (!traverse_module_state) return 0;
  Py_VISIT(traverse_module_state->__pyx_d);
  Py_VISIT(traverse_module_state->__pyx_b);
  Py_VISIT(traverse_module_state->__pyx_cython_runtime);
  Py_VISIT(traverse_module_state->__pyx_empty_tuple);
  Py_VISIT(traverse_module_state->__pyx_empty_bytes);
  Py_VISIT(traverse_module_state->__pyx_empty_unicode);
  #ifdef __Pyx_CyFunction_USED
  Py_VISIT(traverse_module_state->__pyx_CyFunctionType);
  #endif
  #ifdef __Pyx_FusedFunction_USED
  Py_VISIT(traverse_module_state->__pyx_FusedFunctionType);
  #endif
  Py_VISIT(traverse_module_state->__pyx_ptype_4qutk___pyx_scope_struct__index);
  Py_VISIT(traverse_module_state->__pyx_type_4qutk___pyx_scope_struct__index);
  Py_VISIT(traverse_module_state->__pyx_ptype_4qutk___pyx_scope_struct_1_miu);
  Py_VISIT(traverse_module_state->__pyx_type_4qutk___pyx_scope_struct_1_miu);
  Py_VISIT(traverse_module_state->__pyx_n_s_);
  Py_VISIT(traverse_module_state->__pyx_n_s_A);
  Py_VISIT(traverse_module_state->__pyx_kp_s_A_absolute_passability);
  Py_VISIT(traverse_module_state->__pyx_n_s_Lq);
  Py_VISIT(traverse_module_state->__pyx_kp_s_Lq_average_waiting_queue_length);
  Py_VISIT(traverse_module_state->__pyx_n_s_Ls);
  Py_VISIT(traverse_module_state->__pyx_kp_s_Ls_average_queue_length_the_aver);
  Py_VISIT(traverse_module_state->__pyx_kp_s_M_M_1);
  Py_VISIT(traverse_module_state->__pyx_kp_s_M_M_i);
  Py_VISIT(traverse_module_state->__pyx_n_s_P);
  Py_VISIT(traverse_module_state->__pyx_n_s_P0);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P0_the_probability_of_system_idl);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P_N_i);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P_N_i_the_probability_of_more_th);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P_T_f);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P_T_g_the_probability_of_staying);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P_i);
  Py_VISIT(traverse_module_state->__pyx_kp_s_P_i_the_probability_of_i_in_cust);
  Py_VISIT(traverse_module_state->__pyx_n_s_Plost);
  Py_VISIT(traverse_module_state->__pyx_kp_s_Plost_the_probability_of_system);
  Py_VISIT(traverse_module_state->__pyx_n_s_Q);
  Py_VISIT(traverse_module_state->__pyx_kp_s_Q_relative_passability);
  Py_VISIT(traverse_module_state->__pyx_n_s_Wq);
  Py_VISIT(traverse_module_state->__pyx_kp_s_Wq_average_waiting_time);
  Py_VISIT(traverse_module_state->__pyx_n_s_Ws);
  Py_VISIT(traverse_module_state->__pyx_kp_s_Ws_average_staying_time_average);
  Py_VISIT(traverse_module_state->__pyx_kp_s__10);
  Py_VISIT(traverse_module_state->__pyx_kp_s__11);
  Py_VISIT(traverse_module_state->__pyx_kp_u__12);
  Py_VISIT(traverse_module_state->__pyx_n_s__13);
  Py_VISIT(traverse_module_state->__pyx_n_s__14);
  Py_VISIT(traverse_module_state->__pyx_n_s__2);
  Py_VISIT(traverse_module_state->__pyx_n_s__24);
  Py_VISIT(traverse_module_state->__pyx_kp_s__3);
  Py_VISIT(traverse_module_state->__pyx_kp_s__8);
  Py_VISIT(traverse_module_state->__pyx_kp_s__9);
  Py_VISIT(traverse_module_state->__pyx_n_s_asyncio_coroutines);
  Py_VISIT(traverse_module_state->__pyx_kp_s_average_service_rate_per_server);
  Py_VISIT(traverse_module_state->__pyx_n_s_best);
  Py_VISIT(traverse_module_state->__pyx_n_s_ceil);
  Py_VISIT(traverse_module_state->__pyx_n_s_class_getitem);
  Py_VISIT(traverse_module_state->__pyx_n_s_cline_in_traceback);
  Py_VISIT(traverse_module_state->__pyx_n_s_cost);
  Py_VISIT(traverse_module_state->__pyx_n_s_d);
  Py_VISIT(traverse_module_state->__pyx_n_s_detail);
  Py_VISIT(traverse_module_state->__pyx_kp_u_disable);
  Py_VISIT(traverse_module_state->__pyx_kp_s_e);
  Py_VISIT(traverse_module_state->__pyx_kp_s_e_system_average_effective_arriv);
  Py_VISIT(traverse_module_state->__pyx_kp_u_enable);
  Py_VISIT(traverse_module_state->__pyx_n_s_exp);
  Py_VISIT(traverse_module_state->__pyx_n_s_factorial);
  Py_VISIT(traverse_module_state->__pyx_n_s_fsolve);
  Py_VISIT(traverse_module_state->__pyx_kp_u_gc);
  Py_VISIT(traverse_module_state->__pyx_n_s_i);
  Py_VISIT(traverse_module_state->__pyx_n_s_import);
  Py_VISIT(traverse_module_state->__pyx_n_s_index);
  Py_VISIT(traverse_module_state->__pyx_n_s_index_locals_P);
  Py_VISIT(traverse_module_state->__pyx_n_s_indices);
  Py_VISIT(traverse_module_state->__pyx_n_s_inf);
  Py_VISIT(traverse_module_state->__pyx_n_s_initializing);
  Py_VISIT(traverse_module_state->__pyx_n_s_is_coroutine);
  Py_VISIT(traverse_module_state->__pyx_kp_u_isenabled);
  Py_VISIT(traverse_module_state->__pyx_n_s_join);
  Py_VISIT(traverse_module_state->__pyx_n_s_k);
  Py_VISIT(traverse_module_state->__pyx_n_s_main);
  Py_VISIT(traverse_module_state->__pyx_n_s_math);
  Py_VISIT(traverse_module_state->__pyx_n_s_max);
  Py_VISIT(traverse_module_state->__pyx_n_s_max_queue);
  Py_VISIT(traverse_module_state->__pyx_n_s_max_wait);
  Py_VISIT(traverse_module_state->__pyx_n_s_method);
  Py_VISIT(traverse_module_state->__pyx_n_s_min_cost);
  Py_VISIT(traverse_module_state->__pyx_n_s_miu);
  Py_VISIT(traverse_module_state->__pyx_n_s_miu_locals_lambda);
  Py_VISIT(traverse_module_state->__pyx_n_s_model);
  Py_VISIT(traverse_module_state->__pyx_n_s_n);
  Py_VISIT(traverse_module_state->__pyx_n_s_n_queue_max);
  Py_VISIT(traverse_module_state->__pyx_n_s_n_server);
  Py_VISIT(traverse_module_state->__pyx_n_s_n_server_max);
  Py_VISIT(traverse_module_state->__pyx_n_s_name);
  Py_VISIT(traverse_module_state->__pyx_n_s_qutk);
  Py_VISIT(traverse_module_state->__pyx_kp_s_qutk_py);
  Py_VISIT(traverse_module_state->__pyx_n_s_range);
  Py_VISIT(traverse_module_state->__pyx_n_s_remark);
  Py_VISIT(traverse_module_state->__pyx_n_s_return_detail);
  Py_VISIT(traverse_module_state->__pyx_n_s_s);
  Py_VISIT(traverse_module_state->__pyx_n_s_s_2);
  Py_VISIT(traverse_module_state->__pyx_n_s_s_3);
  Py_VISIT(traverse_module_state->__pyx_n_s_scipy_optimize);
  Py_VISIT(traverse_module_state->__pyx_n_s_server_cost);
  Py_VISIT(traverse_module_state->__pyx_kp_s_server_efficiency);
  Py_VISIT(traverse_module_state->__pyx_n_s_server_income);
  Py_VISIT(traverse_module_state->__pyx_kp_s_service_intensity_the_probabili);
  Py_VISIT(traverse_module_state->__pyx_n_s_spec);
  Py_VISIT(traverse_module_state->__pyx_n_s_split);
  Py_VISIT(traverse_module_state->__pyx_n_s_sum);
  Py_VISIT(traverse_module_state->__pyx_kp_s_system_average_arrival_rate_the);
  Py_VISIT(traverse_module_state->__pyx_n_s_t);
  Py_VISIT(traverse_module_state->__pyx_n_s_t_wait_max);
  Py_VISIT(traverse_module_state->__pyx_n_s_test);
  Py_VISIT(traverse_module_state->__pyx_n_s_update);
  Py_VISIT(traverse_module_state->__pyx_n_s_wait_cost);
  Py_VISIT(traverse_module_state->__pyx_n_s_z);
  Py_VISIT(traverse_module_state->__pyx_n_s_zip);
  Py_VISIT(traverse_module_state->__pyx_float_0_5);
  Py_VISIT(traverse_module_state->__pyx_int_0);
  Py_VISIT(traverse_module_state->__pyx_int_1);
  Py_VISIT(traverse_module_state->__pyx_int_2);
  Py_VISIT(traverse_module_state->__pyx_int_4);
  Py_VISIT(traverse_module_state->__pyx_int_100);
  Py_VISIT(traverse_module_state->__pyx_int_neg_1);
  Py_VISIT(traverse_module_state->__pyx_slice__4);
  Py_VISIT(traverse_module_state->__pyx_tuple__5);
  Py_VISIT(traverse_module_state->__pyx_tuple__7);
  Py_VISIT(traverse_module_state->__pyx_tuple__15);
  Py_VISIT(traverse_module_state->__pyx_tuple__17);
  Py_VISIT(traverse_module_state->__pyx_tuple__18);
  Py_VISIT(traverse_module_state->__pyx_tuple__20);
  Py_VISIT(traverse_module_state->__pyx_tuple__21);
  Py_VISIT(traverse_module_state->__pyx_tuple__23);
  Py_VISIT(traverse_module_state->__pyx_codeobj__6);
  Py_VISIT(traverse_module_state->__pyx_codeobj__16);
  Py_VISIT(traverse_module_state->__pyx_codeobj__19);
  Py_VISIT(traverse_module_state->__pyx_codeobj__22);
  return 0;
}
#endif

#define __pyx_d __pyx_mstate_global->__pyx_d
#define __pyx_b __pyx_mstate_global->__pyx_b
#define __pyx_cython_runtime __pyx_mstate_global->__pyx_cython_runtime
#define __pyx_empty_tuple __pyx_mstate_global->__pyx_empty_tuple
#define __pyx_empty_bytes __pyx_mstate_global->__pyx_empty_bytes
#define __pyx_empty_unicode __pyx_mstate_global->__pyx_empty_unicode
#ifdef __Pyx_CyFunction_USED
#define __pyx_CyFunctionType __pyx_mstate_global->__pyx_CyFunctionType
#endif
#ifdef __Pyx_FusedFunction_USED
#define __pyx_FusedFunctionType __pyx_mstate_global->__pyx_FusedFunctionType
#endif
#ifdef __Pyx_Generator_USED
#define __pyx_GeneratorType __pyx_mstate_global->__pyx_GeneratorType
#endif
#ifdef __Pyx_IterableCoroutine_USED
#define __pyx_IterableCoroutineType __pyx_mstate_global->__pyx_IterableCoroutineType
#endif
#ifdef __Pyx_Coroutine_USED
#define __pyx_CoroutineAwaitType __pyx_mstate_global->__pyx_CoroutineAwaitType
#endif
#ifdef __Pyx_Coroutine_USED
#define __pyx_CoroutineType __pyx_mstate_global->__pyx_CoroutineType
#endif
#if CYTHON_USE_MODULE_STATE
#define __pyx_type_4qutk___pyx_scope_struct__index __pyx_mstate_global->__pyx_type_4qutk___pyx_scope_struct__index
#define __pyx_type_4qutk___pyx_scope_struct_1_miu __pyx_mstate_global->__pyx_type_4qutk___pyx_scope_struct_1_miu
#endif
#define __pyx_ptype_4qutk___pyx_scope_struct__index __pyx_mstate_global->__pyx_ptype_4qutk___pyx_scope_struct__index
#define __pyx_ptype_4qutk___pyx_scope_struct_1_miu __pyx_mstate_global->__pyx_ptype_4qutk___pyx_scope_struct_1_miu
#define __pyx_n_s_ __pyx_mstate_global->__pyx_n_s_
#define __pyx_n_s_A __pyx_mstate_global->__pyx_n_s_A
#define __pyx_kp_s_A_absolute_passability __pyx_mstate_global->__pyx_kp_s_A_absolute_passability
#define __pyx_n_s_Lq __pyx_mstate_global->__pyx_n_s_Lq
#define __pyx_kp_s_Lq_average_waiting_queue_length __pyx_mstate_global->__pyx_kp_s_Lq_average_waiting_queue_length
#define __pyx_n_s_Ls __pyx_mstate_global->__pyx_n_s_Ls
#define __pyx_kp_s_Ls_average_queue_length_the_aver __pyx_mstate_global->__pyx_kp_s_Ls_average_queue_length_the_aver
#define __pyx_kp_s_M_M_1 __pyx_mstate_global->__pyx_kp_s_M_M_1
#define __pyx_kp_s_M_M_i __pyx_mstate_global->__pyx_kp_s_M_M_i
#define __pyx_n_s_P __pyx_mstate_global->__pyx_n_s_P
#define __pyx_n_s_P0 __pyx_mstate_global->__pyx_n_s_P0
#define __pyx_kp_s_P0_the_probability_of_system_idl __pyx_mstate_global->__pyx_kp_s_P0_the_probability_of_system_idl
#define __pyx_kp_s_P_N_i __pyx_mstate_global->__pyx_kp_s_P_N_i
#define __pyx_kp_s_P_N_i_the_probability_of_more_th __pyx_mstate_global->__pyx_kp_s_P_N_i_the_probability_of_more_th
#define __pyx_kp_s_P_T_f __pyx_mstate_global->__pyx_kp_s_P_T_f
#define __pyx_kp_s_P_T_g_the_probability_of_staying __pyx_mstate_global->__pyx_kp_s_P_T_g_the_probability_of_staying
#define __pyx_kp_s_P_i __pyx_mstate_global->__pyx_kp_s_P_i
#define __pyx_kp_s_P_i_the_probability_of_i_in_cust __pyx_mstate_global->__pyx_kp_s_P_i_the_probability_of_i_in_cust
#define __pyx_n_s_Plost __pyx_mstate_global->__pyx_n_s_Plost
#define __pyx_kp_s_Plost_the_probability_of_system __pyx_mstate_global->__pyx_kp_s_Plost_the_probability_of_system
#define __pyx_n_s_Q __pyx_mstate_global->__pyx_n_s_Q
#define __pyx_kp_s_Q_relative_passability __pyx_mstate_global->__pyx_kp_s_Q_relative_passability
#define __pyx_n_s_Wq __pyx_mstate_global->__pyx_n_s_Wq
#define __pyx_kp_s_Wq_average_waiting_time __pyx_mstate_global->__pyx_kp_s_Wq_average_waiting_time
#define __pyx_n_s_Ws __pyx_mstate_global->__pyx_n_s_Ws
#define __pyx_kp_s_Ws_average_staying_time_average __pyx_mstate_global->__pyx_kp_s_Ws_average_staying_time_average
#define __pyx_kp_s__10 __pyx_mstate_global->__pyx_kp_s__10
#define __pyx_kp_s__11 __pyx_mstate_global->__pyx_kp_s__11
#define __pyx_kp_u__12 __pyx_mstate_global->__pyx_kp_u__12
#define __pyx_n_s__13 __pyx_mstate_global->__pyx_n_s__13
#define __pyx_n_s__14 __pyx_mstate_global->__pyx_n_s__14
#define __pyx_n_s__2 __pyx_mstate_global->__pyx_n_s__2
#define __pyx_n_s__24 __pyx_mstate_global->__pyx_n_s__24
#define __pyx_kp_s__3 __pyx_mstate_global->__pyx_kp_s__3
#define __pyx_kp_s__8 __pyx_mstate_global->__pyx_kp_s__8
#define __pyx_kp_s__9 __pyx_mstate_global->__pyx_kp_s__9
#define __pyx_n_s_asyncio_coroutines __pyx_mstate_global->__pyx_n_s_asyncio_coroutines
#define __pyx_kp_s_average_service_rate_per_server __pyx_mstate_global->__pyx_kp_s_average_service_rate_per_server
#define __pyx_n_s_best __pyx_mstate_global->__pyx_n_s_best
#define __pyx_n_s_ceil __pyx_mstate_global->__pyx_n_s_ceil
#define __pyx_n_s_class_getitem __pyx_mstate_global->__pyx_n_s_class_getitem
#define __pyx_n_s_cline_in_traceback __pyx_mstate_global->__pyx_n_s_cline_in_traceback
#define __pyx_n_s_cost __pyx_mstate_global->__pyx_n_s_cost
#define __pyx_n_s_d __pyx_mstate_global->__pyx_n_s_d
#define __pyx_n_s_detail __pyx_mstate_global->__pyx_n_s_detail
#define __pyx_kp_u_disable __pyx_mstate_global->__pyx_kp_u_disable
#define __pyx_kp_s_e __pyx_mstate_global->__pyx_kp_s_e
#define __pyx_kp_s_e_system_average_effective_arriv __pyx_mstate_global->__pyx_kp_s_e_system_average_effective_arriv
#define __pyx_kp_u_enable __pyx_mstate_global->__pyx_kp_u_enable
#define __pyx_n_s_exp __pyx_mstate_global->__pyx_n_s_exp
#define __pyx_n_s_factorial __pyx_mstate_global->__pyx_n_s_factorial
#define __pyx_n_s_fsolve __pyx_mstate_global->__pyx_n_s_fsolve
#define __pyx_kp_u_gc __pyx_mstate_global->__pyx_kp_u_gc
#define __pyx_n_s_i __pyx_mstate_global->__pyx_n_s_i
#define __pyx_n_s_import __pyx_mstate_global->__pyx_n_s_import
#define __pyx_n_s_index __pyx_mstate_global->__pyx_n_s_index
#define __pyx_n_s_index_locals_P __pyx_mstate_global->__pyx_n_s_index_locals_P
#define __pyx_n_s_indices __pyx_mstate_global->__pyx_n_s_indices
#define __pyx_n_s_inf __pyx_mstate_global->__pyx_n_s_inf
#define __pyx_n_s_initializing __pyx_mstate_global->__pyx_n_s_initializing
#define __pyx_n_s_is_coroutine __pyx_mstate_global->__pyx_n_s_is_coroutine
#define __pyx_kp_u_isenabled __pyx_mstate_global->__pyx_kp_u_isenabled
#define __pyx_n_s_join __pyx_mstate_global->__pyx_n_s_join
#define __pyx_n_s_k __pyx_mstate_global->__pyx_n_s_k
#define __pyx_n_s_main __pyx_mstate_global->__pyx_n_s_main
#define __pyx_n_s_math __pyx_mstate_global->__pyx_n_s_math
#define __pyx_n_s_max __pyx_mstate_global->__pyx_n_s_max
#define __pyx_n_s_max_queue __pyx_mstate_global->__pyx_n_s_max_queue
#define __pyx_n_s_max_wait __pyx_mstate_global->__pyx_n_s_max_wait
#define __pyx_n_s_method __pyx_mstate_global->__pyx_n_s_method
#define __pyx_n_s_min_cost __pyx_mstate_global->__pyx_n_s_min_cost
#define __pyx_n_s_miu __pyx_mstate_global->__pyx_n_s_miu
#define __pyx_n_s_miu_locals_lambda __pyx_mstate_global->__pyx_n_s_miu_locals_lambda
#define __pyx_n_s_model __pyx_mstate_global->__pyx_n_s_model
#define __pyx_n_s_n __pyx_mstate_global->__pyx_n_s_n
#define __pyx_n_s_n_queue_max __pyx_mstate_global->__pyx_n_s_n_queue_max
#define __pyx_n_s_n_server __pyx_mstate_global->__pyx_n_s_n_server
#define __pyx_n_s_n_server_max __pyx_mstate_global->__pyx_n_s_n_server_max
#define __pyx_n_s_name __pyx_mstate_global->__pyx_n_s_name
#define __pyx_n_s_qutk __pyx_mstate_global->__pyx_n_s_qutk
#define __pyx_kp_s_qutk_py __pyx_mstate_global->__pyx_kp_s_qutk_py
#define __pyx_n_s_range __pyx_mstate_global->__pyx_n_s_range
#define __pyx_n_s_remark __pyx_mstate_global->__pyx_n_s_remark
#define __pyx_n_s_return_detail __pyx_mstate_global->__pyx_n_s_return_detail
#define __pyx_n_s_s __pyx_mstate_global->__pyx_n_s_s
#define __pyx_n_s_s_2 __pyx_mstate_global->__pyx_n_s_s_2
#define __pyx_n_s_s_3 __pyx_mstate_global->__pyx_n_s_s_3
#define __pyx_n_s_scipy_optimize __pyx_mstate_global->__pyx_n_s_scipy_optimize
#define __pyx_n_s_server_cost __pyx_mstate_global->__pyx_n_s_server_cost
#define __pyx_kp_s_server_efficiency __pyx_mstate_global->__pyx_kp_s_server_efficiency
#define __pyx_n_s_server_income __pyx_mstate_global->__pyx_n_s_server_income
#define __pyx_kp_s_service_intensity_the_probabili __pyx_mstate_global->__pyx_kp_s_service_intensity_the_probabili
#define __pyx_n_s_spec __pyx_mstate_global->__pyx_n_s_spec
#define __pyx_n_s_split __pyx_mstate_global->__pyx_n_s_split
#define __pyx_n_s_sum __pyx_mstate_global->__pyx_n_s_sum
#define __pyx_kp_s_system_average_arrival_rate_the __pyx_mstate_global->__pyx_kp_s_system_average_arrival_rate_the
#define __pyx_n_s_t __pyx_mstate_global->__pyx_n_s_t
#define __pyx_n_s_t_wait_max __pyx_mstate_global->__pyx_n_s_t_wait_max
#define __pyx_n_s_test __pyx_mstate_global->__pyx_n_s_test
#define __pyx_n_s_update __pyx_mstate_global->__pyx_n_s_update
#define __pyx_n_s_wait_cost __pyx_mstate_global->__pyx_n_s_wait_cost
#define __pyx_n_s_z __pyx_mstate_global->__pyx_n_s_z
#define __pyx_n_s_zip __pyx_mstate_global->__pyx_n_s_zip
#define __pyx_float_0_5 __pyx_mstate_global->__pyx_float_0_5
#define __pyx_int_0 __pyx_mstate_global->__pyx_int_0
#define __pyx_int_1 __pyx_mstate_global->__pyx_int_1
#define __pyx_int_2 __pyx_mstate_global->__pyx_int_2
#define __pyx_int_4 __pyx_mstate_global->__pyx_int_4
#define __pyx_int_100 __pyx_mstate_global->__pyx_int_100
#define __pyx_int_neg_1 __pyx_mstate_global->__pyx_int_neg_1
#define __pyx_slice__4 __pyx_mstate_global->__pyx_slice__4
#define __pyx_tuple__5 __pyx_mstate_global->__pyx_tuple__5
#define __pyx_tuple__7 __pyx_mstate_global->__pyx_tuple__7
#define __pyx_tuple__15 __pyx_mstate_global->__pyx_tuple__15
#define __pyx_tuple__17 __pyx_mstate_global->__pyx_tuple__17
#define __pyx_tuple__18 __pyx_mstate_global->__pyx_tuple__18
#define __pyx_tuple__20 __pyx_mstate_global->__pyx_tuple__20
#define __pyx_tuple__21 __pyx_mstate_global->__pyx_tuple__21
#define __pyx_tuple__23 __pyx_mstate_global->__pyx_tuple__23
#define __pyx_codeobj__6 __pyx_mstate_global->__pyx_codeobj__6
#define __pyx_codeobj__16 __pyx_mstate_global->__pyx_codeobj__16
#define __pyx_codeobj__19 __pyx_mstate_global->__pyx_codeobj__19
#define __pyx_codeobj__22 __pyx_mstate_global->__pyx_codeobj__22





static PyObject *__pyx_pw_4qutk_1index(PyObject *__pyx_self, 
#if CYTHON_METH_FASTCALL
PyObject *const *__pyx_args, Py_ssize_t __pyx_nargs, PyObject *__pyx_kwds
#else
PyObject *__pyx_args, PyObject *__pyx_kwds
#endif
); 
PyDoc_STRVAR(__pyx_doc_4qutk_index, "\n    \316\273\n    \316\274\n    n=None\n    t=None\n    model='M/M/1/\342\210\236'\n    ");
static PyMethodDef __pyx_mdef_4qutk_1index = {"index", (PyCFunction)(void*)(__Pyx_PyCFunction_FastCallWithKeywords)__pyx_pw_4qutk_1index, __Pyx_METH_FASTCALL|METH_KEYWORDS, __pyx_doc_4qutk_index};
static PyObject *__pyx_pw_4qutk_1index(PyObject *__pyx_self, 
#if CYTHON_METH_FASTCALL
PyObject *const *__pyx_args, Py_ssize_t __pyx_nargs, PyObject *__pyx_kwds
#else
PyObject *__pyx_args, PyObject *__pyx_kwds
#endif
) {
  PyObject *__pyx_Uv__5cg = 0;
  PyObject *__pyx_Uv__fdg = 0;
  PyObject *__pyx_v_n = 0;
  PyObject *__pyx_v_t = 0;
  PyObject *__pyx_v_model = 0;
  #if !CYTHON_METH_FASTCALL
  CYTHON_UNUSED Py_ssize_t __pyx_nargs;
  #endif
  CYTHON_UNUSED PyObject *const *__pyx_kwvalues;
  PyObject* values[5] = {0,0,0,0,0};
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  PyObject *__pyx_r = 0;
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("index (wrapper)", 0);
  #if !CYTHON_METH_FASTCALL
  #if CYTHON_ASSUME_SAFE_MACROS
  __pyx_nargs = PyTuple_GET_SIZE(__pyx_args);
  #else
  __pyx_nargs = PyTuple_Size(__pyx_args); if (unlikely(__pyx_nargs < 0)) return NULL;
  #endif
  #endif
  __pyx_kwvalues = __Pyx_KwValues_FASTCALL(__pyx_args, __pyx_nargs);
  {
    PyObject **__pyx_pyargnames[] = {&__pyx_n_s_,&__pyx_n_s__2,&__pyx_n_s_n,&__pyx_n_s_t,&__pyx_n_s_model,0};
    values[2] = __Pyx_Arg_NewRef_FASTCALL(((PyObject *)Py_None));
    values[3] = __Pyx_Arg_NewRef_FASTCALL(((PyObject *)Py_None));
    values[4] = __Pyx_Arg_NewRef_FASTCALL(((PyObject *)((PyObject*)__pyx_kp_s_M_M_1)));
    if (__pyx_kwds) {
      Py_ssize_t kw_args;
      switch (__pyx_nargs) {
        case  5: values[4] = __Pyx_Arg_FASTCALL(__pyx_args, 4);
        CYTHON_FALLTHROUGH;
        case  4: values[3] = __Pyx_Arg_FASTCALL(__pyx_args, 3);
        CYTHON_FALLTHROUGH;
        case  3: values[2] = __Pyx_Arg_FASTCALL(__pyx_args, 2);
        CYTHON_FALLTHROUGH;
        case  2: values[1] = __Pyx_Arg_FASTCALL(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = __Pyx_Arg_FASTCALL(__pyx_args, 0);
        CYTHON_FALLTHROUGH;
        case  0: break;
        default: goto __pyx_L5_argtuple_error;
      }
      kw_args = __Pyx_NumKwargs_FASTCALL(__pyx_kwds);
      switch (__pyx_nargs) {
        case  0:
        if (likely((values[0] = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_)) != 0)) {
          (void)__Pyx_Arg_NewRef_FASTCALL(values[0]);
          kw_args--;
        }
        else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 9, __pyx_L3_error)
        else goto __pyx_L5_argtuple_error;
        CYTHON_FALLTHROUGH;
        case  1:
        if (likely((values[1] = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s__2)) != 0)) {
          (void)__Pyx_Arg_NewRef_FASTCALL(values[1]);
          kw_args--;
        }
        else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 9, __pyx_L3_error)
        else {
          __Pyx_RaiseArgtupleInvalid("index", 0, 2, 5, 1); __PYX_ERR(0, 9, __pyx_L3_error)
        }
        CYTHON_FALLTHROUGH;
        case  2:
        if (kw_args > 0) {
          PyObject* value = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_n);
          if (value) { values[2] = __Pyx_Arg_NewRef_FASTCALL(value); kw_args--; }
          else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 9, __pyx_L3_error)
        }
        CYTHON_FALLTHROUGH;
        case  3:
        if (kw_args > 0) {
          PyObject* value = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_t);
          if (value) { values[3] = __Pyx_Arg_NewRef_FASTCALL(value); kw_args--; }
          else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 9, __pyx_L3_error)
        }
        CYTHON_FALLTHROUGH;
        case  4:
        if (kw_args > 0) {
          PyObject* value = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_model);
          if (value) { values[4] = __Pyx_Arg_NewRef_FASTCALL(value); kw_args--; }
          else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 9, __pyx_L3_error)
        }
      }
      if (unlikely(kw_args > 0)) {
        const Py_ssize_t kwd_pos_args = __pyx_nargs;
        if (unlikely(__Pyx_ParseOptionalKeywords(__pyx_kwds, __pyx_kwvalues, __pyx_pyargnames, 0, values + 0, kwd_pos_args, "index") < 0)) __PYX_ERR(0, 9, __pyx_L3_error)
      }
    } else {
      switch (__pyx_nargs) {
        case  5: values[4] = __Pyx_Arg_FASTCALL(__pyx_args, 4);
        CYTHON_FALLTHROUGH;
        case  4: values[3] = __Pyx_Arg_FASTCALL(__pyx_args, 3);
        CYTHON_FALLTHROUGH;
        case  3: values[2] = __Pyx_Arg_FASTCALL(__pyx_args, 2);
        CYTHON_FALLTHROUGH;
        case  2: values[1] = __Pyx_Arg_FASTCALL(__pyx_args, 1);
        values[0] = __Pyx_Arg_FASTCALL(__pyx_args, 0);
        break;
        default: goto __pyx_L5_argtuple_error;
      }
    }
    __pyx_Uv__5cg = values[0];
    __pyx_Uv__fdg = values[1];
    __pyx_v_n = values[2];
    __pyx_v_t = values[3];
    __pyx_v_model = values[4];
  }
  goto __pyx_L6_skip;
  __pyx_L5_argtuple_error:;
  __Pyx_RaiseArgtupleInvalid("index", 0, 2, 5, __pyx_nargs); __PYX_ERR(0, 9, __pyx_L3_error)
  __pyx_L6_skip:;
  goto __pyx_L4_argument_unpacking_done;
  __pyx_L3_error:;
  {
    Py_ssize_t __pyx_temp;
    for (__pyx_temp=0; __pyx_temp < (Py_ssize_t)(sizeof(values)/sizeof(values[0])); ++__pyx_temp) {
      __Pyx_Arg_XDECREF_FASTCALL(values[__pyx_temp]);
    }
  }
  __Pyx_AddTraceback("qutk.index", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __Pyx_RefNannyFinishContext();
  return NULL;
  __pyx_L4_argument_unpacking_done:;
  __pyx_r = __pyx_pf_4qutk_index(__pyx_self, __pyx_Uv__5cg, __pyx_Uv__fdg, __pyx_v_n, __pyx_v_t, __pyx_v_model);

  
  {
    Py_ssize_t __pyx_temp;
    for (__pyx_temp=0; __pyx_temp < (Py_ssize_t)(sizeof(values)/sizeof(values[0])); ++__pyx_temp) {
      __Pyx_Arg_XDECREF_FASTCALL(values[__pyx_temp]);
    }
  }
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}




static PyObject *__pyx_pw_4qutk_5index_1P(PyObject *__pyx_self, 
#if CYTHON_METH_FASTCALL
PyObject *const *__pyx_args, Py_ssize_t __pyx_nargs, PyObject *__pyx_kwds
#else
PyObject *__pyx_args, PyObject *__pyx_kwds
#endif
); 
static PyMethodDef __pyx_mdef_4qutk_5index_1P = {"P", (PyCFunction)(void*)(__Pyx_PyCFunction_FastCallWithKeywords)__pyx_pw_4qutk_5index_1P, __Pyx_METH_FASTCALL|METH_KEYWORDS, 0};
static PyObject *__pyx_pw_4qutk_5index_1P(PyObject *__pyx_self, 
#if CYTHON_METH_FASTCALL
PyObject *const *__pyx_args, Py_ssize_t __pyx_nargs, PyObject *__pyx_kwds
#else
PyObject *__pyx_args, PyObject *__pyx_kwds
#endif
) {
  PyObject *__pyx_v_n = 0;
  PyObject *__pyx_v_s = 0;
  PyObject *__pyx_v_k = 0;
  #if !CYTHON_METH_FASTCALL
  CYTHON_UNUSED Py_ssize_t __pyx_nargs;
  #endif
  CYTHON_UNUSED PyObject *const *__pyx_kwvalues;
  PyObject* values[3] = {0,0,0};
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  PyObject *__pyx_r = 0;
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("P (wrapper)", 0);
  #if !CYTHON_METH_FASTCALL
  #if CYTHON_ASSUME_SAFE_MACROS
  __pyx_nargs = PyTuple_GET_SIZE(__pyx_args);
  #else
  __pyx_nargs = PyTuple_Size(__pyx_args); if (unlikely(__pyx_nargs < 0)) return NULL;
  #endif
  #endif
  __pyx_kwvalues = __Pyx_KwValues_FASTCALL(__pyx_args, __pyx_nargs);
  {
    PyObject **__pyx_pyargnames[] = {&__pyx_n_s_n,&__pyx_n_s_s,&__pyx_n_s_k,0};
    values[1] = __Pyx_Arg_NewRef_FASTCALL(((PyObject *)((PyObject *)__pyx_int_1)));
    values[2] = __Pyx_Arg_NewRef_FASTCALL(((PyObject *)Py_None));
    if (__pyx_kwds) {
      Py_ssize_t kw_args;
      switch (__pyx_nargs) {
        case  3: values[2] = __Pyx_Arg_FASTCALL(__pyx_args, 2);
        CYTHON_FALLTHROUGH;
        case  2: values[1] = __Pyx_Arg_FASTCALL(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = __Pyx_Arg_FASTCALL(__pyx_args, 0);
        CYTHON_FALLTHROUGH;
        case  0: break;
        default: goto __pyx_L5_argtuple_error;
      }
      kw_args = __Pyx_NumKwargs_FASTCALL(__pyx_kwds);
      switch (__pyx_nargs) {
        case  0:
        if (likely((values[0] = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_n)) != 0)) {
          (void)__Pyx_Arg_NewRef_FASTCALL(values[0]);
          kw_args--;
        }
        else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 21, __pyx_L3_error)
        else goto __pyx_L5_argtuple_error;
        CYTHON_FALLTHROUGH;
        case  1:
        if (kw_args > 0) {
          PyObject* value = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_s);
          if (value) { values[1] = __Pyx_Arg_NewRef_FASTCALL(value); kw_args--; }
          else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 21, __pyx_L3_error)
        }
        CYTHON_FALLTHROUGH;
        case  2:
        if (kw_args > 0) {
          PyObject* value = __Pyx_GetKwValue_FASTCALL(__pyx_kwds, __pyx_kwvalues, __pyx_n_s_k);
          if (value) { values[2] = __Pyx_Arg_NewRef_FASTCALL(value); kw_args--; }
          else if (unlikely(PyErr_Occurred())) __PYX_ERR(0, 21, __pyx_L3_error)
        }
      }
      if (unlikely(kw_args > 0)) {
        const Py_ssize_t kwd_pos_args = __pyx_nargs;
        if (unlikely(__Pyx_ParseOptionalKeywords(__pyx_kwds, __pyx_kwvalues, __pyx_pyargnames, 0, values + 0, kwd_pos_args, "P") < 0)) __PYX_ERR(0, 21, __pyx_L3_error)
      }
    } else {
      switch (__pyx_nargs) {
        case  3: values[2] = __Pyx_Arg_FASTCALL(__pyx_args, 2);
        CYTHON_FALLTHROUGH;
        case  2: values[1] = __Pyx_Arg_FASTCALL(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = __Pyx_Arg_FASTCALL(__pyx_args, 0);
        break;
        default: goto __pyx_L5_argtuple_error;
      }
    }
    __pyx_v_n = values[0];
    __pyx_v_s = values[1];
    __pyx_v_k = values[2];
  }
  goto __pyx_L6_skip;
  __pyx_L5_argtuple_error:;
  __Pyx_RaiseArgtupleInvalid("P", 0, 1, 3, __pyx_nargs); __PYX_ERR(0, 21, __pyx_L3_error)
  __pyx_L6_skip:;
  goto __pyx_L4_argument_unpacking_done;
  __pyx_L3_error:;
  {
    Py_ssize_t __pyx_temp;
    for (__pyx_temp=0; __pyx_temp < (Py_ssize_t)(sizeof(values)/sizeof(values[0])); ++__pyx_temp) {
      __Pyx_Arg_XDECREF_FASTCALL(values[__pyx_temp]);
    }
  }
  __Pyx_AddTraceback("qutk.index.P", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __Pyx_RefNannyFinishContext();
  return NULL;
  __pyx_L4_argument_unpacking_done:;
  __pyx_r = __pyx_pf_4qutk_5index_P(__pyx_self, __pyx_v_n, __pyx_v_s, __pyx_v_k);

  
  {
    Py_ssize_t __pyx_temp;
    for (__pyx_temp=0; __pyx_temp < (Py_ssize_t)(sizeof(values)/sizeof(values[0])); ++__pyx_temp) {
      __Pyx_Arg_XDECREF_FASTCALL(values[__pyx_temp]);
    }
  }
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

static PyObject *__pyx_pf_4qutk_5index_P(PyObject *__pyx_self, PyObject *__pyx_v_n, PyObject *__pyx_v_s, PyObject *__pyx_v_k) {
  struct __pyx_obj_4qutk___pyx_scope_struct__index *__pyx_cur_scope;
  struct __pyx_obj_4qutk___pyx_scope_struct__index *__pyx_outer_scope;
  PyObject *__pyx_r = NULL;
  __Pyx_RefNannyDeclarations
  PyObject *__pyx_t_1 = NULL;
  int __pyx_t_2;
  PyObject *__pyx_t_3 = NULL;
  PyObject *__pyx_t_4 = NULL;
  PyObject *__pyx_t_5 = NULL;
  int __pyx_t_6;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  __Pyx_RefNannySetupContext("P", 1);
