__int64 __fastcall sub_14474F1C0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rdi
  char *v5; // rdi
  __int64 v6; // rsi
  __int64 v7; // r14
  __int64 v8; // r8
  _BYTE v10[33]; // [rsp+27h] [rbp-21h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v10, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
  {
    LODWORD(v5) = 0;
    return (unsigned int)v5;
  }
  v6 = *a2;
  if ( v6 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v6 + 8));
    v5 = (char *)(a1 + 6);
    v7 = a1 + 9;
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: a1 + 6, a3: 3);
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: a1, a3: 4);
    v8 = 1;
    if ( v10[0] >= 2u )
    {
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v7, a3: 1);
      v8 = 2;
      v7 = a1 + 4;
    }
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v7, a3: v8);
    if ( *v5 < 27 )
      goto LABEL_8;
    goto LABEL_7;
  }
  v5 = (char *)(a1 + 6);
  if ( *(char *)(a1 + 6) >= 27 )
LABEL_7:
    *v5 = -1;
LABEL_8:
  LOBYTE(v5) = *(_DWORD *)(v6 + 16) == 0;
  if ( _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
  return (unsigned int)v5;
}
