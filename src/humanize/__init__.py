"""
Humanize library - Convert data into human-readable formats
"""
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
import math


def intcomma(value, ndigits=None):
    """
    Convert an integer to a string with comma separators.
    
    Example: 1234567 -> '1,234,567'
    """
    try:
        if ndigits:
            value = round(float(value), ndigits)
        
        orig = str(value)
        
        if '.' in orig:
            int_part, dec_part = orig.split('.')
            result = _add_commas(int_part)
            return f"{result}.{dec_part}"
        else:
            return _add_commas(orig)
    except (ValueError, TypeError):
        return str(value)


def _add_commas(value_str):
    """Helper to add commas to integer string"""
    if value_str.startswith('-'):
        sign = '-'
        value_str = value_str[1:]
    else:
        sign = ''
    
    result = []
    for i, digit in enumerate(reversed(value_str)):
        if i and i % 3 == 0:
            result.append(',')
        result.append(digit)
    
    return sign + ''.join(reversed(result))


def intword(value, format='%.1f'):
    """
    Convert a large integer to a friendly text representation.
    
    Example: 1000000 -> '1.0 million'
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return str(value)
    
    if value < 0:
        sign = '-'
        value = abs(value)
    else:
        sign = ''
    
    if value < 1000:
        return sign + str(value)
    
    powers = [
        (10 ** 12, 'trillion'),
        (10 ** 9, 'billion'),
        (10 ** 6, 'million'),
        (10 ** 3, 'thousand'),
    ]
    
    for power, word in powers:
        if value >= power:
            chopped = value / float(power)
            return sign + (format % chopped) + ' ' + word
    
    return sign + str(value)


def apnumber(value):
    """
    For numbers 0-9, return the word. Otherwise, return the number.
    
    Example: 4 -> 'four', 10 -> '10'
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return str(value)
    
    if not 0 <= value <= 9:
        return str(value)
    
    words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    return words[value]


def ordinal(value):
    """
    Convert an integer to its ordinal as a string.
    
    Example: 1 -> '1st', 2 -> '2nd', 3 -> '3rd', 4 -> '4th'
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return str(value)
    
    if 10 <= value % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
    
    return f"{value}{suffix}"


def naturalsize(value, binary=False, gnu=False, format='%.1f'):
    """
    Format a number of bytes as a human-readable file size.
    
    Example: 1000000 -> '1.0 MB'
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return str(value)
    
    if value < 0:
        sign = '-'
        value = abs(value)
    else:
        sign = ''
    
    if binary:
        base = 1024
        if gnu:
            suffixes = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
        else:
            suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    else:
        base = 1000
        suffixes = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    
    if value < base:
        if gnu:
            return f"{sign}{value}"
        return f"{sign}{value} {suffixes[0]}"
    
    for i, suffix in enumerate(suffixes[1:], 1):
        unit = base ** i
        if value < unit * base or i == len(suffixes) - 1:
            if gnu:
                return f"{sign}{format % (value / unit)}{suffix}"
            else:
                return f"{sign}{format % (value / unit)} {suffix}"
    
    return f"{sign}{value} bytes"


def naturaltime(value, future=False, months=True, minimum_unit="seconds", when=None):
    """
    Return a natural representation of a time delta.
    
    Example: datetime.now() - timedelta(seconds=3600) -> 'an hour ago'
    """
    if when is None:
        when = datetime.now()
    
    if isinstance(value, timedelta):
        delta = value
    elif isinstance(value, datetime):
        delta = when - value if not future else value - when
    else:
        return str(value)
    
    seconds = delta.total_seconds()
    
    if seconds < 0:
        seconds = abs(seconds)
        suffix = 'from now'
    else:
        suffix = 'ago'
    
    if seconds < 1:
        if minimum_unit in ['microseconds', 'milliseconds']:
            ms = delta.total_seconds() * 1000
            if ms < 1:
                return f"{int(delta.total_seconds() * 1000000)} microseconds {suffix}"
            return f"{int(ms)} milliseconds {suffix}"
        return 'now'
    
    if seconds < 60:
        if seconds == 1:
            return f"a second {suffix}"
        return f"{int(seconds)} seconds {suffix}"
    
    minutes = seconds / 60
    if minutes < 60:
        if int(minutes) == 1:
            return f"a minute {suffix}"
        return f"{int(minutes)} minutes {suffix}"
    
    hours = minutes / 60
    if hours < 24:
        if int(hours) == 1:
            return f"an hour {suffix}"
        return f"{int(hours)} hours {suffix}"
    
    days = hours / 24
    if days < 7:
        if int(days) == 1:
            return f"a day {suffix}"
        return f"{int(days)} days {suffix}"
    
    weeks = days / 7
    if weeks < 4.35:
        if int(weeks) == 1:
            return f"a week {suffix}"
        return f"{int(weeks)} weeks {suffix}"
    
    if months:
        months_val = days / 30.5
        if months_val < 12:
            if int(months_val) == 1:
                return f"a month {suffix}"
            return f"{int(months_val)} months {suffix}"
        
        years = months_val / 12
        if int(years) == 1:
            return f"a year {suffix}"
        return f"{int(years)} years {suffix}"
    
    return f"{int(days)} days {suffix}"


def naturaldelta(value, months=True, minimum_unit="seconds"):
    """
    Return a natural representation of a time delta (without 'ago' suffix).
    
    Example: timedelta(seconds=3600) -> 'an hour'
    """
    if isinstance(value, timedelta):
        seconds = value.total_seconds()
    else:
        try:
            seconds = float(value)
        except (ValueError, TypeError):
            return str(value)
    
    seconds = abs(seconds)
    
    if seconds < 1:
        if minimum_unit in ['microseconds', 'milliseconds']:
            ms = seconds * 1000
            if ms < 1:
                return f"{int(seconds * 1000000)} microseconds"
            return f"{int(ms)} milliseconds"
        return 'a moment'
    
    if seconds < 60:
        if int(seconds) == 1:
            return "a second"
        return f"{int(seconds)} seconds"
    
    minutes = seconds / 60
    if minutes < 60:
        if int(minutes) == 1:
            return "a minute"
        return f"{int(minutes)} minutes"
    
    hours = minutes / 60
    if hours < 24:
        if int(hours) == 1:
            return "an hour"
        return f"{int(hours)} hours"
    
    days = hours / 24
    if days < 7:
        if int(days) == 1:
            return "a day"
        return f"{int(days)} days"
    
    weeks = days / 7
    if weeks < 4.35:
        if int(weeks) == 1:
            return "a week"
        return f"{int(weeks)} weeks"
    
    if months:
        months_val = days / 30.5
        if months_val < 12:
            if int(months_val) == 1:
                return "a month"
            return f"{int(months_val)} months"
        
        years = months_val / 12
        if int(years) == 1:
            return "a year"
        return f"{int(years)} years"
    
    return f"{int(days)} days"


def naturalday(value, format='%b %d'):
    """
    For date values that are tomorrow, today or yesterday, return the natural text.
    Otherwise, return a formatted date string.
    
    Example: date.today() -> 'today'
    """
    if isinstance(value, datetime):
        value = value.date()
    
    try:
        from datetime import date
        today = date.today()
        
        if value == today:
            return 'today'
        elif value == today - timedelta(days=1):
            return 'yesterday'
        elif value == today + timedelta(days=1):
            return 'tomorrow'
        else:
            return value.strftime(format)
    except (AttributeError, TypeError):
        return str(value)


def naturaldate(value):
    """
    Like naturalday, but appends year for dates outside current year.
    
    Example: date(2007, 6, 5) -> 'Jun 05 2007'
    """
    if isinstance(value, datetime):
        value = value.date()
    
    try:
        from datetime import date
        today = date.today()
        
        if value == today:
            return 'today'
        elif value == today - timedelta(days=1):
            return 'yesterday'
        elif value == today + timedelta(days=1):
            return 'tomorrow'
        elif value.year == today.year:
            return value.strftime('%b %d')
        else:
            return value.strftime('%b %d %Y')
    except (AttributeError, TypeError):
        return str(value)


def precisedelta(value, minimum_unit="seconds", suppress=None, format="%.2f"):
    """
    Return a precise representation of a time delta.
    
    Example: timedelta(seconds=3633, days=2) -> '2 days, 1 hour and 33.00 seconds'
    """
    if not isinstance(value, timedelta):
        return str(value)
    
    if suppress is None:
        suppress = []
    
    total_seconds = abs(value.total_seconds())
    
    units = []
    
    # Days
    if 'days' not in suppress:
        days = int(total_seconds // 86400)
        if days:
            units.append(f"{days} day{'s' if days != 1 else ''}")
            total_seconds -= days * 86400
    
    # Hours
    if 'hours' not in suppress:
        hours = int(total_seconds // 3600)
        if hours:
            units.append(f"{hours} hour{'s' if hours != 1 else ''}")
            total_seconds -= hours * 3600
    
    # Minutes
    if 'minutes' not in suppress:
        minutes = int(total_seconds // 60)
        if minutes:
            units.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            total_seconds -= minutes * 60
    
    # Seconds
    if 'seconds' not in suppress:
        if total_seconds or not units:
            if minimum_unit == 'microseconds':
                seconds = format % total_seconds
                units.append(f"{seconds} seconds")
            elif minimum_unit == 'milliseconds':
                seconds = format % total_seconds
                units.append(f"{seconds} seconds")
            else:
                seconds = format % total_seconds
                units.append(f"{seconds} second{'s' if float(seconds) != 1 else ''}")
    
    if not units:
        return '0 seconds'
    
    if len(units) == 1:
        return units[0]
    elif len(units) == 2:
        return f"{units[0]} and {units[1]}"
    else:
        return ', '.join(units[:-1]) + f' and {units[-1]}'


def fractional(value):
    """
    Convert a float to a fraction representation.
    
    Example: 0.5 -> '1/2', 1.5 -> '1 1/2'
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    if value == int(value):
        return str(int(value))
    
    frac = Fraction(value).limit_denominator(1000)
    
    if frac.numerator > frac.denominator:
        whole = frac.numerator // frac.denominator
        remainder = frac.numerator % frac.denominator
        if remainder == 0:
            return str(whole)
        return f"{whole} {remainder}/{frac.denominator}"
    else:
        return f"{frac.numerator}/{frac.denominator}"


def scientific(value, precision=2):
    """
    Return a number in scientific notation.
    
    Example: 500 -> '5.00 x 10²'
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    if value == 0:
        return f"0.{'0' * precision} x 10⁰"
    
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    
    superscript = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '-': '⁻'
    }
    
    exp_str = ''.join(superscript[c] for c in str(exponent))
    
    if precision == 0:
        return f"{int(mantissa)} x 10{exp_str}"
    else:
        return f"{mantissa:.{precision}f} x 10{exp_str}"


__all__ = [
    'intcomma', 'intword', 'apnumber', 'ordinal',
    'naturalsize', 'naturaltime', 'naturaldelta',
    'naturalday', 'naturaldate', 'precisedelta',
    'fractional', 'scientific'
]