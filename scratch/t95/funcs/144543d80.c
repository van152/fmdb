__int64 __fastcall sub_144543D80(__int64 a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, int a7, __int64 a8)
{
  _DWORD *v11; // rsi
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // rsi
  __int64 v15; // rsi

  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 24, 4);
  if ( v11[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 4);
  if ( v12[4] != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 44, 2);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 46, 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 40, 4);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  else
    return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
