__int64 __fastcall sub_1415D8860(__int64 a1, _QWORD *a2, unsigned __int8 a3, unsigned int a4)
{
  _DWORD *v4; // rbp
  __int64 v8; // rsi
  _DWORD *v9; // rdi
  bool v10; // bp
  __int64 v11; // rdi
  __int64 v12; // rdi
  __int64 v13; // rdi
  __int64 v14; // rdi
  __int64 v15; // rdi
  __int64 v16; // rdi
  __int64 v17; // rdi
  __int64 v18; // rdx
  _BYTE v20[7]; // [rsp+20h] [rbp-38h] BYREF
  char v21[49]; // [rsp+27h] [rbp-31h] BYREF

  v8 = a1 + -*(_DWORD *)(a1 - 4);
  if ( a3 == 0 )
  {
    LOBYTE(v4) = 1;
    if ( (_BYTE)a4 == 0 )
      return (unsigned int)v4;
    goto LABEL_6;
  }
  v4 = (_DWORD *)*a2;
  v21[0] = 6;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: v21, a3: 1);
  if ( v4[4] != 0 )
  {
LABEL_23:
    LODWORD(v4) = 0;
    return (unsigned int)v4;
  }
  if ( (_BYTE)a4 != 0 )
  {
LABEL_6:
    sub_140F9F4A0(a1: v20);
    v9 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 16, a3: 1);
    v10 = true;
    if ( v9[4] == 0 )
    {
      v11 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 14, a3: 1);
      if ( *(_DWORD *)(v11 + 16) == 0 )
      {
        v12 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 13, a3: 1);
        if ( *(_DWORD *)(v12 + 16) == 0 && (unsigned __int8)sub_140F81F40(a1: *(_QWORD *)(v8 - 24), a2, a3: 1) != 0 )
        {
          v13 = *a2;
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 15, a3: 1);
          v10 = *(_DWORD *)(v13 + 16) != 0;
        }
      }
    }
    if ( v20[0] == 0 )
      byte_141B5FC2C = 0;
    if ( (v10 | a3 ^ 1) != 0 )
    {
      LOBYTE(v4) = !v10;
      return (unsigned int)v4;
    }
  }
  LODWORD(v4) = 0;
  if ( (unsigned __int8)sub_140DFC460(a1: v8 - 16, a2, a3: 0, a4) != 0 )
  {
    v14 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 + 24, a3: 8);
    if ( *(_DWORD *)(v14 + 16) == 0 )
    {
      v15 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 + 8, a3: 4);
      if ( *(_DWORD *)(v15 + 16) == 0 )
      {
        v16 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 + 12, a3: 4);
        if ( *(_DWORD *)(v16 + 16) == 0 )
        {
          v17 = *a2;
          v18 = *(_DWORD *)(v8 + 16) != 0 ? v8 + 16 : v8 + 12;
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v18, a3: 4);
          if ( *(_DWORD *)(v17 + 16) == 0 )
          {
            LOBYTE(v4) = 1;
            return (unsigned int)v4;
          }
        }
      }
    }
    goto LABEL_23;
  }
  return (unsigned int)v4;
}
