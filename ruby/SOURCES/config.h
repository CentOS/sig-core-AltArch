/*
 * This config.h is a wrapper include file for the original ruby/config.h,
 * which has been renamed to ruby/config-<arch>.h. There are conflicts for the
 * original ruby/config.h on multilib systems, which result from arch-specific
 * configuration options. Please do not use the arch-specific file directly.
 */

/*
 * This wrapped is addpated from SDL's one:
 * http://pkgs.fedoraproject.org/cgit/SDL.git/tree/SDL_config.h
 */

#ifdef ruby_config_wrapper_h
#error "ruby_config_wrapper_h should not be defined!"
#endif
#define ruby_config_wrapper_h

#if defined(__i386__)
#include "ruby/config-i386.h"
#elif defined(__ia64__)
#include "ruby/config-ia64.h"
#elif defined(__powerpc64__)
#include <endian.h>
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "ruby/config-ppc64.h"
#else
#include "ruby/config-ppc64le.h"
#endif
#elif defined(__powerpc__)
#include "ruby/config-ppc.h"
#elif defined(__s390x__)
#include "ruby/config-s390x.h"
#elif defined(__s390__)
#include "ruby/config-s390.h"
#elif defined(__x86_64__)
#include "ruby/config-x86_64.h"
#elif defined(__arm__)
#include "ruby/config-arm.h"
#elif defined(__alpha__)
#include "ruby/config-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "ruby/config-sparc64.h"
#elif defined(__sparc__)
#include "ruby/config-sparc.h"
#elif defined(__aarch64__)
#include "ruby/config-aarch64.h"
#else
#error "The ruby-devel package is not usable with the architecture."
#endif

#undef ruby_config_wrapper_h
