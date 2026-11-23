char __fastcall sub_144016370(__int64 a1, _DWORD *a2, unsigned int a3, char a4, unsigned __int8 a5, unsigned int a6)
{
  _QWORD *v10; // rbx
  char v11; // bp
  __int64 v12; // rax
  char result; // al
  unsigned __int64 v14; // rcx
  __int64 v15; // rbp
  __int64 v16; // rsi
  signed __int32 v17; // et0
  __int64 v18; // rax
  _QWORD v19[2]; // [rsp+28h] [rbp-C0h] BYREF
  __int64 v20; // [rsp+38h] [rbp-B0h]
  _BYTE v21[24]; // [rsp+40h] [rbp-A8h] BYREF
  _BYTE v22[24]; // [rsp+58h] [rbp-90h] BYREF
  _BYTE v23[32]; // [rsp+70h] [rbp-78h] BYREF
  __int64 v24; // [rsp+90h] [rbp-58h]
  int v25; // [rsp+A0h] [rbp-48h]
  char v26; // [rsp+A6h] [rbp-42h]
  char v27; // [rsp+A8h] [rbp-40h]

  sub_1415577E0(v19);
  sub_141557910(v19, a1, a3);
  if ( a2 != nullptr )
  {
    v10 = (_QWORD *)(*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a2 + 1024LL))(a2, a1, 0);
    if ( v10 != nullptr )
    {
LABEL_3:
      v11 = (*(__int64 (__fastcall **)(_QWORD *))(*v10 + 80LL))(v10);
      v12 = v10[2];
LABEL_7:
      v25 = a2[2];
      v26 = v11;
      v24 = v12;
      goto LABEL_8;
    }
    if ( *(_BYTE *)(a1 + 186) != 0 || (v18 = sub_140E68C40(a1)) == 0 )
    {
      v11 = 0;
    }
    else
    {
      v11 = 0;
      v10 = (_QWORD *)(*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a2 + 1024LL))(a2, v18, 0);
      if ( v10 != nullptr )
        goto LABEL_3;
    }
    v12 = 0;
    goto LABEL_7;
  }
LABEL_8:
  v27 = a4;
  sub_1415583E0(v19, a1, a6, a5);
  sub_14083B0A0(v23);
  sub_14083B0A0(v22);
  result = sub_14083B0A0(v21);
  if ( v19[0] == 0 )
    return result;
  v14 = v20 - v19[0];
  if ( v20 - v19[0] == -1 )
  {
    v14 = *(unsigned int *)(v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      return MEMORY[0x141948990](v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    return MEMORY[0x141948990](v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
  }
  v15 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v15) >> 3 <= v14 )
    return MEMORY[0x141948990](v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
  v16 = *(_QWORD *)(v15 + 8 * v14);
  if ( v16 == 0 )
    return MEMORY[0x141948990](v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
  MEMORY[0x1419475D8](v16 + 32, v19[0] - *(unsigned int *)(v16 + 120));
  if ( *(_BYTE *)(v16 + 72) != 0 )
  {
    v17 = _InterlockedDecrement((volatile signed __int32 *)(v16 + 64));
    result = v17 != 0;
    if ( v17 != 0 )
      return result;
  }
  else
  {
    result = 0;
  }
  if ( *(_BYTE *)(v16 + 97) != 0 )
    return sub_1412D33C0(v16);
  return result;
}
