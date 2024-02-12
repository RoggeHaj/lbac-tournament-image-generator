#!/usr/bin/env python3

import argparse
import os
import random
import subprocess
import sys
import xml.etree.ElementTree as ET

from datetime import datetime


valid_genders = ['herr', 'dam']
valid_tournament_types = ['grön', 'svart', 'challenger']


def parse_args():
    """Parse arguments provided to program"""

    parser = argparse.ArgumentParser(
        prog='SoMe content generator',
        description='Generates LBAC ads for Social Media',
        epilog='Yes')

    parser.add_argument('--date',
                        action='store',
                        default='tournament_template.svg',
                        dest='date',
                        help='Date for the tournament',
                        required=True
                        )

    parser.add_argument('--level',
                        action='store',
                        choices=valid_tournament_types,
                        default=valid_tournament_types[0],
                        dest='tournament_level',
                        help='Tournament level',
                        nargs='?',
                        required=False
                        )

    parser.add_argument('--gender',
                        action='store',
                        choices=valid_genders,
                        default=valid_genders[0],
                        dest='gender',
                        help='Gender for the tournament',
                        nargs='?',
                        required=False
                        )

    parser.add_argument('--template',
                        action='store',
                        default='tournament_template.svg',
                        dest='template',
                        help='Name of the template file to use',
                        nargs='?',
                        required=False
                        )

    args = parser.parse_args()

    try:
        real_date = datetime.strptime(args.date, '%Y-%m-%d')
        args.date = real_date

    except ValueError as e:
        print('date needs to be in format yyyy-mm-dd and be a valid date.\n', file=sys.stderr)
        sys.exit(1)

    return args


def type2star(tournament_type):
    """Return tournament type as star ranking"""
    tournament_map = {
        'grön': '1*',
        'svart': '2*',
        'challenger': '3*',
    }

    return tournament_map[tournament_type]


def type2text(tournament_type):
    """Return long text for tournament type"""
    tournament_map = {
        'grön': 'Open Grön',
        'svart': 'Open Svart',
        'challenger': 'Challenger'
    }

    return tournament_map[tournament_type]


def date2weekday(my_date, short = False):
    """Return proper weekday name for provided date"""
    week_days = [
        'söndagen',
        'måndagen',
        'tisdagen',
        'onsdagen',
        'torsdagen',
        'fredagen',
        'lördagen',
    ]

    week_day = week_days[int(my_date.strftime("%w"))]

    if short:
        week_day = week_day[:3]

    return week_day


def date2day(my_date):
    """Return date in month for provided date"""
    return my_date.strftime('%d')


def date2month(my_date, short = False):
    """Return month name for provided date"""
    months = [
        'januari',
        'februari',
        'mars',
        'april',
        'maj',
        'juni',
        'juli',
        'augusti',
        'september',
        'oktober',
        'november',
        'december',
    ]

    month = months[int(my_date.strftime('%m')) - 1]

    if short:
        month = month[:3]

    return month


def format_text(args):
    """Swap text anchors from template to proper contents"""
    n_stars = type2star(args.tournament_level)
    uc_tournament_type = type2text(args.tournament_level).upper()
    uc_gender = args.gender.upper()
    weekday = date2weekday(args.date)
    date = date2day(args.date)
    month = date2month(args.date)
    short_month = date2month(args.date, True).capitalize()

    with open(args.template, 'r') as svgfile:
        svg_contents = svgfile.read()

    svg_contents = svg_contents.replace('@DATE@', date)
    svg_contents = svg_contents.replace('@SHORT_MONTH@', short_month)
    svg_contents = svg_contents.replace('@STARS@', n_stars)
    svg_contents = svg_contents.replace('@GENDER@', args.gender)
    svg_contents = svg_contents.replace('@DAY@', weekday)
    svg_contents = svg_contents.replace('@MONTH@', month)
    svg_contents = svg_contents.replace('@UC_GENDER@', uc_gender)
    svg_contents = svg_contents.replace('@TYPE@', uc_tournament_type)

    return svg_contents


def select_background(svgdata, gender):
    """Select a background with id similar to selected gender"""
    image = ET.fromstring(svgdata)
    image_list = []

    for elm in image.findall('.//*[@id="Background"]/{http://www.w3.org/2000/svg}image'):
        if gender in elm.attrib['id']:
            image_list.append(elm)

    elm = image_list[random.randint(1, len(image_list)) - 1]
    elm.attrib['style'] = elm.attrib['style'].replace('display:none', 'display:normal')

    return ET.tostring(image, encoding='unicode')


def write_file(svgdata, args):
    """Write the generated SVG to file"""
    outdir = 'generated-contents'
    filename = f'{args.date.strftime("%Y-%m-%d")}_{args.gender}'
    tmpfile = f'{filename}.svg'
    outfile = f'{outdir}{os.sep}{filename}.png'

    os.makedirs(outdir, exist_ok=True)

    with open(tmpfile, 'w') as f:
        f.write(svgdata)

    subprocess.run(['inkscape', '-o', outfile, tmpfile], check=True)

    os.remove(tmpfile)


def main():
    """Main routine"""
    args = parse_args()
    svgdata = format_text(args)
    svgdata = select_background(svgdata, args.gender)

    write_file(svgdata, args)


if __name__ == '__main__':
    main()
