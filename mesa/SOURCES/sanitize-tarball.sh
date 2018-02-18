#!/bin/sh
#
# usage: sanitize-tarball.sh [tarball]

if [ "x$1" = "x" ]; then
    echo "Usage: sanitize-tarball.sh [tarball]"
    exit 1
fi

if [ -e /usr/bin/pxz ]; then
    XZ=/usr/bin/pxz
else
    XZ=/usr/bin/xz
fi

dirname=$(basename $(basename "$1" .tar.bz2) .tar.xz)

tar xf "$1"
pushd $dirname

cat > src/gallium/auxiliary/vl/vl_mpeg12_decoder.c << EOF
#include "vl_mpeg12_decoder.h"
struct pipe_video_codec *
vl_create_mpeg12_decoder(struct pipe_context *context,
		const struct pipe_video_codec *templat)
{
    return NULL;
}
EOF

cat > src/gallium/auxiliary/vl/vl_decoder.c << EOF
#include "vl_decoder.h"
bool vl_profile_supported(struct pipe_screen *screen,
                          enum pipe_video_profile profile,
			enum pipe_video_entrypoint entrypoint)
{
    return false;
}

int
vl_level_supported(struct pipe_screen *screen, enum pipe_video_profile profile)
{
   return 0;
}

struct pipe_video_codec *
vl_create_decoder(struct pipe_context *pipe,
	const struct pipe_video_codec *templat)
{
    return NULL;
}
EOF

popd
tar cf - $dirname | $XZ > $dirname.tar.xz
