char __fastcall sub_143D904B0(__int64 a1, _QWORD *a2, _QWORD *a3, __int64 a4, int a5)
{
  int v8; // edi
  _DWORD *v9; // rsi
  int v10; // eax
  char v11; // al
  __int64 v12; // r8
  char result; // al
  __int64 v14; // rsi
  _QWORD *v15; // rbx
  char v16; // [rsp+2Bh] [rbp-2Dh] BYREF
  int v17[11]; // [rsp+2Ch] [rbp-2Ch] BYREF

  v8 = a1;
  v9 = (_DWORD *)*a3;
  v10 = *(_DWORD *)(*a3 + 12LL);
  if ( (v10 & 2) == 0 )
  {
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: &v16, a3: 1);
    if ( v9[4] == 0 )
    {
      v11 = v16;
      goto LABEL_16;
    }
    return 0;
  }
  if ( *(_BYTE *)(a1 + 1450) != 0 || a5 == 1 && *(_BYTE *)(a1 + 1451) != 0 )
  {
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      v12 = 4;
    else
      v12 = 8;
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2, a3: v12);
    return v9[4] == 0;
  }
  v11 = (2 * ~(_BYTE)v10) & 4;
  if ( byte_141AAE088 == 0 )
    v11 = 0;
  v16 = v11;
LABEL_16:
  *a2 = 0;
  if ( v11 != 0 )
    return sub_140F85110(a1: v8, (_DWORD)a2, (_DWORD)a3, a4, a5: v11);
  v14 = *a3;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: v17, a3: 4);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  result = 1;
  if ( v17[0] != 0xFFFFFFFFLL )
  {
    if ( v17[0] >= 0 )
    {
      v15 = *(_QWORD **)(a4 + 128);
      if ( (__int64)(v15[1] - *v15) >> 3 > (unsigned __int64)(unsigned int)v17[0] )
      {
        *a2 = *(_QWORD *)(*v15 + 8LL * (unsigned int)v17[0]);
        return result;
      }
    }
    return 0;
  }
  return result;
}
