bool __fastcall sub_143F89580(__int64 a1, _QWORD *a2, char a3, char a4)
{
  _DWORD *v8; // rsi
  bool result; // al
  __int64 v10; // rsi
  __int64 v11; // rsi
  __int64 v12; // rsi
  _DWORD *v13; // rdi
  __int64 v14; // rdx
  char v15; // [rsp+2Fh] [rbp-39h] BYREF
  int v16; // [rsp+30h] [rbp-38h] BYREF
  _DWORD v17[12]; // [rsp+38h] [rbp-30h] BYREF

  if ( a3 == 0 )
  {
    result = true;
    if ( a4 == 0 )
      return result;
LABEL_6:
    sub_1408149D0(a1: *a2, a2: v17, a3: a1 + 32);
    if ( v17[0] != 0 )
      return false;
    sub_1408149D0(a1: *a2, a2: &v16, a3: a1 + 40);
    result = v16 == 0;
    if ( v16 != 0 )
      return result;
    goto LABEL_8;
  }
  v8 = (_DWORD *)*a2;
  v15 = 5;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: &v15, a3: 1);
  if ( v8[4] != 0 )
    return false;
  if ( a4 != 0 )
    goto LABEL_6;
  result = true;
LABEL_8:
  if ( a3 == 0 )
    return result;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 24, a3: 8);
  if ( *(_DWORD *)(v10 + 16) == 0 )
  {
    v11 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
    if ( *(_DWORD *)(v11 + 16) == 0 )
    {
      v12 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 12, a3: 4);
      if ( *(_DWORD *)(v12 + 16) == 0 )
      {
        v13 = (_DWORD *)*a2;
        v14 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v13 + 40LL))(a1: v13, a2: v14, a3: 4);
        if ( v13[4] == 0 )
          return true;
      }
    }
  }
  return false;
}
