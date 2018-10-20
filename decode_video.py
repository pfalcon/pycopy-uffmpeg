# Based on decode_video.c example from FFmpeg distribution
#
# Copyright (c) 2001 Fabrice Bellard
# Copyright (c) 2018 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import uctypes
from uffmpeg import *
from uerrno import EAGAIN


avcodec_register_all()

pkt = av_packet_alloc()
print("pkt addr:", hex(pkt))
pkt = uctypes.struct(pkt, AVPacket_layout)
print("pkt:", pkt)

codec = avcodec_find_decoder(AV_CODEC_ID_H264);
print("codec:", hex(codec))

parser = av_parser_init(AV_CODEC_ID_H264);
print("parser:", hex(parser))

ctx = avcodec_alloc_context3(codec)
print("ctx:", hex(ctx))

print("code open res:", avcodec_open2(ctx, codec, NULL))

frame = av_frame_alloc()
print("frame addr:", hex(frame))
frame = uctypes.struct(frame, AVFrame_layout)
print("frame:", frame)


frame_cnt = 0

frame_num = 20

def pgm_save(buf, wrap, xsize, ysize, fname):
    with open(fname, "wb") as f:
        f.write("P5\n%d %d\n%d\n" % (xsize, ysize, 255))
        for i in range(ysize):
            f.write(uctypes.bytearray_at(int(buf) + i * wrap, xsize))


def decode(dec_ctx, frame, pkt):
    print("\ndecode: dec_ctx: %s, frame: %s, pkt: %s" % (dec_ctx, frame, pkt))
    ret = avcodec_send_packet(dec_ctx, pkt)
    print("send pkt ret:", ret)
    assert ret >= 0

    while ret >= 0:
        ret = avcodec_receive_frame(dec_ctx, frame)
        print("rcv frm:", ret, hex(ret))

        if ret == AVERROR(EAGAIN) or ret == AVERROR_EOF:
            print("decode: ret")
            return
        assert ret >= 0

#        print("saving frame %3d, fmt: %d, pict_type: %d\n", dec_ctx.frame_number, frame.format, frame.pict_type);
        print("saving frame ??, fmt: %d, pict_type: %d" % (frame.format, frame.pict_type));

        global frame_cnt
        pgm_save(frame.data[0], frame.linesize[0],
                 frame.width, frame.height, "frame-%03d.pgm" % frame_cnt);
        frame_cnt += 1


with open(sys.argv[1], "rb") as f:
    while True:
        buf = f.read(4096)
        if not buf:
            break

        membuf = memoryview(buf)
        offset = 0

        while True:
#            data_size = len(buf)
#            if not data_size:
#                break
            data = membuf[offset:]
            if not data:
                break
            print("feeding:", len(data))
            print(hex(uctypes.addressof(pkt, "data")), hex(uctypes.addressof(pkt, "size")))

            ret = av_parser_parse2(parser, ctx,
                uctypes.addressof(pkt, "data"),
                uctypes.addressof(pkt, "size"),
                data, len(data), AV_NOPTS_VALUE, AV_NOPTS_VALUE, 0)
            print("consumed:", ret)
            assert ret >= 0
            offset += ret

            print("pkt.size", pkt.size, pkt.data) #, bytes(pkt.data))
            if pkt.size:
                decode(ctx, frame, pkt)
                if frame_cnt == frame_num:
                    sys.exit()
