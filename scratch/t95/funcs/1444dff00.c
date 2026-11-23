__int64 __fastcall sub_1444DFF00(__int64 a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, int a7, __int64 a8)
{
  _DWORD *v11; // rsi
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  _DWORD v15[10]; // [rsp+20h] [rbp-28h] BYREF

  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 24, 4);
  if ( v11[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 4);
  if ( v12[4] != 0 )
    return 0;
  if ( (unsigned __int8)sub_141726770(a1 + 48, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_141726770(a1 + 72, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_141726770(a1 + 96, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_141726770(a1 + 120, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1 + 40, a2) == 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 44, 4);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  sub_141541000(v15, a2, a1 + 144);
  if ( v15[0] != 0 )
    return 0;
  sub_141541480(v15, a2, a1 + 168);
  if ( v15[0] != 0 )
    return 0;
  sub_141541000(v15, a2, a1 + 192);
  if ( v15[0] != 0 )
    return 0;
  sub_141541480(v15, a2, a1 + 216);
  if ( v15[0] != 0 )
    return 0;
  else
    return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
