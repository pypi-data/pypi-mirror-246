#!/usr/bin/python
# Copyright 2019 by Armoha.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from typing import Literal, overload

from ... import core as c
from ... import ctrlstru as cs
from ... import utils as ut
from ...core.eudfunc.eudf import _EUDPredefineParam
from ...core.variable.evcommon import _cp
from ...localize import _
from ..memiof import f_dwread_cp, f_posread_cp, f_setcurpl2cpcache

_loct = ut.EPD(0x58DC60) - 5


def _locfgen2(mod1, mod2, mod3, mod4, signed=False):
    @c.EUDFunc
    def _locf(epd, x, y):
        act = c.Forward()

        c.VProc(
            [epd, x],
            [epd.AddNumber(_loct), epd.SetDest(ut.EPD(act) + 4)]
            + [
                x.SetDest(ut.EPD(act) + 5)
                if not signed
                else [
                    c.SetMemory(act + 20, c.SetTo, ~0),
                    x.QueueSubtractTo(ut.EPD(act) + 5),
                ]
            ],
        )
        settb = c.Forward()
        c.RawTrigger(
            nextptr=epd.GetVTable(),
            actions=[
                c.SetMemory(act + 20, c.Add, 1) if signed else [],
                epd.AddNumber(2),
                epd.AddDest(16),
                x.AddDest(16),
                c.SetNextPtr(x.GetVTable(), settb),
                c.SetMemory(x._varact + 24, c.Subtract, 0x02000000) if signed else [],
            ],
        )
        settb << c.NextTrigger()
        c.VProc(
            [epd, y],
            [epd.AddNumber(-1), epd.AddDest(-8)]
            + [
                y.SetDest(ut.EPD(act) + 8 + 5)
                if not signed
                else [
                    c.SetMemory(act + 52, c.SetTo, ~0),
                    y.QueueSubtractTo(ut.EPD(act) + 8 + 5),
                ]
            ],
        )
        setcoords = c.Forward()
        c.RawTrigger(
            nextptr=epd.GetVTable(),
            actions=[
                c.SetMemory(act + 52, c.Add, 1) if signed else [],
                epd.AddNumber(2),
                epd.AddDest(16),
                y.AddDest(16),
                c.SetNextPtr(y.GetVTable(), setcoords),
                c.SetMemory(y._varact + 24, c.Subtract, 0x02000000) if signed else [],
            ],
        )
        setcoords << c.NextTrigger()
        c.RawTrigger(
            actions=[
                act << c.SetDeaths(0, mod1, 0, 0),
                c.SetDeaths(0, mod2, 0, 0),
                c.SetDeaths(0, mod3, 0, 0),
                c.SetDeaths(0, mod4, 0, 0),
            ]
        )

    return _locf


def _locfgen4(mod1, mod2, mod3, mod4, signed=False):
    @c.EUDFunc
    def _locf(epd, l, t, r, b):
        act = c.Forward()

        c.VProc(
            [epd, l],
            [epd.AddNumber(_loct), epd.SetDest(ut.EPD(act) + 4)]
            + [
                l.SetDest(ut.EPD(act) + 5)
                if not signed
                else [
                    c.SetMemory(act + 20, c.SetTo, ~0),
                    l.QueueSubtractTo(ut.EPD(act) + 5),
                ]
            ],
        )
        c.VProc(
            [epd, t],
            [
                c.SetMemory(act + 20, c.Add, 1) if signed else [],
                epd.AddNumber(1),
                epd.AddDest(8),
                t.SetDest(ut.EPD(act) + 8 + 5)
                if not signed
                else [
                    c.SetMemory(act + 52, c.SetTo, ~0),
                    t.QueueSubtractTo(ut.EPD(act) + 8 + 5),
                ],
            ],
        )
        c.VProc(
            [epd, r],
            [
                c.SetMemory(act + 52, c.Add, 1) if signed else [],
                epd.AddNumber(1),
                epd.AddDest(8),
                r.SetDest(ut.EPD(act) + 16 + 5),
            ],
        )
        c.VProc(
            [epd, b],
            [epd.AddNumber(1), epd.AddDest(8), b.SetDest(ut.EPD(act) + 24 + 5)],
        )
        c.RawTrigger(
            actions=[
                act << c.SetDeaths(0, mod1, 0, 0),
                c.SetDeaths(0, mod2, 0, 0),
                c.SetDeaths(0, mod3, 0, 0),
                c.SetDeaths(0, mod4, 0, 0),
            ]
        )

    return _locf


_SetLoc2 = _locfgen2(c.SetTo, c.SetTo, c.SetTo, c.SetTo)
_AddLoc2 = _locfgen2(c.Add, c.Add, c.Add, c.Add)
_DilateLoc2 = _locfgen2(c.Add, c.Add, c.Add, c.Add, signed=True)
_SetLoc4 = _locfgen4(c.SetTo, c.SetTo, c.SetTo, c.SetTo)
_AddLoc4 = _locfgen4(c.Add, c.Add, c.Add, c.Add)
_DilateLoc4 = _locfgen4(c.Add, c.Add, c.Add, c.Add, signed=True)


@overload
def f_setloc(locID, *coords, action: Literal[True]) -> list[c.Action]:
    ...


@overload
def f_setloc(locID, *coords, action: Literal[False]) -> None:
    ...


def f_setloc(locID, *coords, action=False):
    ut.ep_assert(
        len(coords) == 2 or len(coords) == 4,
        _("number of coordinates should be 2 or 4."),
    )
    locID = c.EncodeLocation(locID)
    if action is True:
        ut.ep_assert(all(c.IsConstExpr(x) for x in coords) and c.IsConstExpr(locID))
    if c.IsConstExpr(locID):
        dst = _loct + 5 * locID
        if len(coords) == 2:
            l, t = coords
            r, b = coords
        else:
            l, t, r, b = coords
        if action is True:
            return [c.SetMemoryEPD(dst + i, c.SetTo, x) for i, x in enumerate((l, t, r, b))]
        c.NonSeqCompute(
            [
                (dst, c.SetTo, l),
                (dst + 1, c.SetTo, t),
                (dst + 2, c.SetTo, r),
                (dst + 3, c.SetTo, b),
            ]
        )
    elif len(coords) == 2:
        _SetLoc2(locID * 5, *coords)
    else:
        _SetLoc4(locID * 5, *coords)


@overload
def f_addloc(locID, *coords, action: Literal[True]) -> list[c.Action]:
    ...


@overload
def f_addloc(locID, *coords, action: Literal[False]) -> None:
    ...


def f_addloc(locID, *coords, action=False):
    ut.ep_assert(
        len(coords) == 2 or len(coords) == 4,
        _("number of coordinates should be 2 or 4."),
    )
    locID = c.EncodeLocation(locID)
    if action is True:
        ut.ep_assert(all(c.IsConstExpr(x) for x in coords) and c.IsConstExpr(locID))
    if c.IsConstExpr(locID):
        dst = _loct + 5 * locID
        if len(coords) == 2:
            l, t = coords
            r, b = coords
        else:
            l, t, r, b = coords
        if action is True:
            return [c.SetMemoryEPD(dst + i, c.Add, x) for i, x in enumerate((l, t, r, b))]
        c.NonSeqCompute(
            [
                (dst, c.Add, l),
                (dst + 1, c.Add, t),
                (dst + 2, c.Add, r),
                (dst + 3, c.Add, b),
            ]
        )
    elif len(coords) == 2:
        _AddLoc2(locID * 5, *coords)
    else:
        _AddLoc4(locID * 5, *coords)


@overload
def f_dilateloc(locID, *coords, action: Literal[True]) -> list[c.Action]:
    ...


@overload
def f_dilateloc(locID, *coords, action: Literal[False]) -> None:
    ...


def f_dilateloc(locID, *coords, action=False):
    ut.ep_assert(
        len(coords) == 2 or len(coords) == 4,
        _("number of coordinates should be 2 or 4."),
    )
    locID = c.EncodeLocation(locID)
    if action is True:
        ut.ep_assert(all(c.IsConstExpr(x) for x in coords) and c.IsConstExpr(locID))
    if c.IsConstExpr(locID):
        dst = _loct + 5 * locID
        if len(coords) == 2:
            l, t = coords
            r, b = coords
        else:
            l, t, r, b = coords
        if action is True:
            return [c.SetMemoryEPD(dst + i, c.Add, x) for i, x in enumerate((-l, -t, r, b))]
        c.NonSeqCompute(
            [
                (dst, c.Add, -l),
                (dst + 1, c.Add, -t),
                (dst + 2, c.Add, r),
                (dst + 3, c.Add, b),
            ]
        )
    elif len(coords) == 2:
        _DilateLoc2(locID * 5, *coords)
    else:
        _DilateLoc4(locID * 5, *coords)


@c.EUDFunc
def _GetLocTL(epd):
    c.VProc(epd, [epd.AddNumber(_loct), epd.SetDest(ut.EPD(0x6509B0))])
    left = f_dwread_cp(0)
    c.RawTrigger(actions=c.SetMemory(0x6509B0, c.Add, 1))
    f_dwread_cp(0, ret=[epd])
    f_setcurpl2cpcache()
    return left, epd


def f_getlocTL(locID, **kwargs) -> tuple[c.EUDVariable, c.EUDVariable]:
    """
    로케이션의 위(top), 왼쪽 (left) 좌표를 얻어냅니다.
    @param  {[type]} locID 로케이션 번호. $L(로케이션 이름) 으로 얻을 수 있습니다.
    """
    locID = c.EncodeLocation(locID)
    return _GetLocTL(locID * 5, **kwargs)


_set_loc: c.Action = c.SetMemory(0x6509B0, c.SetTo, 0)
_setcp2loc: c.ConstExpr = ut.EPD(_set_loc) + 5


@_EUDPredefineParam((_setcp2loc,), c.CurrentPlayer)
@c.EUDFunc
def _SetLocEPD(loc, epd):
    global _setcp2loc
    set_x_epd = c.Forward()
    f_posread_cp(0, ret=[set_x_epd, set_x_epd + 16])

    c.RawTrigger(
        actions=[
            _set_loc,
            c.SetMemory(0x6509B0, c.Add, _loct),
        ]
    )

    set_x = c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0)
    set_xy = c.RawTrigger(
        actions=[
            set_x,
            c.SetMemory(0x6509B0, c.Add, 1),
            c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0),
        ]
    )
    set_x_epd << ut.EPD(set_x) + 5

    done = c.Forward()
    one_more = c.RawTrigger(
        nextptr=set_xy,
        actions=[
            c.SetMemory(0x6509B0, c.Add, 1),
            c.SetNextPtr(set_xy, done),
        ],
    )
    done << f_setcurpl2cpcache(actions=c.SetNextPtr(set_xy, one_more))


def f_setloc_epd(locID, epd) -> None:
    if isinstance(locID, str):
        locID = c.GetLocationIndex(locID)
    _SetLocEPD(locID * 5, epd)
