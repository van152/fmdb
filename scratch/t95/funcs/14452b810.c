__int64 __fastcall sub_14452B810(_QWORD *a1, _QWORD *a2, unsigned int a3, unsigned int a4)
{
  unsigned int v5; // ebx
  _DWORD *v8; // rbp
  _DWORD *v9; // rbp
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbp
  char v14; // [rsp+2Bh] [rbp-2Dh] BYREF
  _DWORD v15[11]; // [rsp+2Ch] [rbp-2Ch] BYREF

  v5 = a3;
  if ( (_BYTE)a3 != 0 )
  {
    v8 = (_DWORD *)*a2;
    v14 = 12;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v8 + 40LL))(v8, &v14, 1);
    if ( v8[4] != 0 )
      return 0;
  }
  v9 = (_DWORD *)*a2;
  v10 = a1[46];
  v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
  v15[0] = v11;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v15, 4);
  if ( v9[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 47, 1);
  if ( v12[4] != 0 )
  {
    return 0;
  }
  else if ( (_BYTE)v5 == 0
         || (v5 = 0, (unsigned __int8)sub_140E5D450(a1, a2, 0, a4) != 0)
         && (v5 = 0, sub_1411D3570((__int64)a1, a2, 0, a4)) )
  {
    LOBYTE(v5) = 1;
  }
  return v5;
}
