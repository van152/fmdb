bool __fastcall sub_1442FFBE0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rsi
  _BYTE *v5; // rbx
  __int64 v6; // rsi
  bool v7; // al
  __int64 v8; // rsi
  __int64 v9; // rsi

  v4 = *a2;
  v5 = (_BYTE *)(a1 + 11);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 11, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0
    || (v6 = *a2,
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 2),
        *(_DWORD *)(v6 + 16) != 0) )
  {
    v7 = false;
    if ( (*v5 & 1) == 0 )
      goto LABEL_4;
LABEL_7:
    if ( v7 )
      goto LABEL_8;
    return false;
  }
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 10, a3: 1);
  v7 = *(_DWORD *)(v8 + 16) == 0;
  if ( (*v5 & 1) != 0 )
    goto LABEL_7;
LABEL_4:
  if ( !v7 )
    return false;
LABEL_8:
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
