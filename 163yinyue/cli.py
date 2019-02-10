from spider import comment, djradio, lyric, music, singer, song, song_sheet, top_list

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--move", '-M', choices=['comment', 'lyric', 'djradio', 'music', 'singer', 'song', 'song_sheet', 'top_list'], type=str)
parser.add_argument("--id", help="id of the song", type=str)
parser.add_argument("--page", help="page of the comment", type=int)
parser.add_argument("--normal", help="normal comments else hot comments, True or False", type=str, choices=['True', 'False'])
parser.add_argument("--show", help="show something", type=str, choices=['True', 'False'])
parser.add_argument("--style", help="style of classify", type=str)

args = parser.parse_args()

if args.move == 'comment' and args.id:
    com = comment.comment()
    if args.page:
        if args.normal == 'True':
            com.get_comment(args.id, args.page)
        else:
            com.get_comment(args.id, args.page, False)
    else:
        com.get_all_comments(args.id)
elif args.move == 'lyric' and args.id:
    lyric = lyric.Lyric()
    lyric.get_lyric(args.id)
elif args.move == 'song_sheet':
    ss = song_sheet.songsheet()
    if args.show:
        ss.show_classify()
    elif args.page:
        if args.style:
            ss.get_songsheet(args.page, args.style)
        else:
            ss.get_songsheet(args.page)
elif args.move == 'singer' and args.id:
    sin = singer.Singer()
    sin.get_singer_introduction(args.id)

