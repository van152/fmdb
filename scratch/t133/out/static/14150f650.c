bool __fastcall sub_14449C2E0(_BYTE *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  unsigned int v6; // eax
  __int64 v7; // rbx
  unsigned int v8; // eax
  __int64 v9; // rbx
  unsigned int v10; // eax
  __int64 v11; // rbx
  unsigned int v12; // eax
  __int64 v13; // rbx
  unsigned int v14; // eax
  __int64 v15; // rbx
  unsigned __int16 v17; // [rsp+24h] [rbp-24h] BYREF
  unsigned __int16 v18; // [rsp+26h] [rbp-22h] BYREF
  unsigned __int16 v19; // [rsp+28h] [rbp-20h] BYREF
  unsigned __int16 v20; // [rsp+2Ah] [rbp-1Eh] BYREF
  unsigned __int16 v21; // [rsp+2Ch] [rbp-1Ch] BYREF
  _BYTE v22[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v22, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v17, a3: 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = v17;
  a1[2] = (v17 >> 7) & 0xF8;
  a1[1] = (v6 >> 2) & 0xF8;
  *a1 = 8 * v6;
  a1[3] = -1;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v18, a3: 2);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = v18;
  a1[6] = (v18 >> 7) & 0xF8;
  a1[5] = (v8 >> 2) & 0xF8;
  a1[4] = 8 * v8;
  a1[7] = -1;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v19, a3: 2);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = v19;
  a1[10] = (v19 >> 7) & 0xF8;
  a1[9] = (v10 >> 2) & 0xF8;
  a1[8] = 8 * v10;
  a1[11] = -1;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v20, a3: 2);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return false;
  v12 = v20;
  a1[14] = (v20 >> 7) & 0xF8;
  a1[13] = (v12 >> 2) & 0xF8;
  a1[12] = 8 * v12;
  a1[15] = -1;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v21, a3: 2);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  v14 = v21;
  a1[18] = (v21 >> 7) & 0xF8;
  a1[17] = (v14 >> 2) & 0xF8;
  a1[16] = 8 * v14;
  a1[19] = -1;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 20, a3: 1);
  return *(_DWORD *)(v15 + 16) == 0 && *(_DWORD *)(*a2 + 16LL) == 0;
}
