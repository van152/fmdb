bool __fastcall sub_143839F90(__int64 a1, char a2, __int64 a3, char a4, char a5)
{
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  int v11; // ecx
  int v12; // edx
  bool result; // al
  __int64 v14; // rax
  __int64 v15; // rax
  __int64 v16; // rax

  if ( a2 != 0 && *(char *)(a1 + 418) > 0 )
    return false;
  v8 = *(_QWORD *)(a1 + 176);
  if ( v8 != 0 && *(_QWORD *)(v8 + 288) != a1 )
    return false;
  if ( (*(_BYTE *)(a1 + 417) & 4) != 0 || *(_WORD *)(a1 + 384) == 0 )
    return false;
  if ( v8 != 0 )
  {
    v9 = *(_QWORD *)(v8 + 1576);
    if ( v9 == 0 )
      goto LABEL_12;
    v10 = *(_QWORD *)(v9 + 288);
  }
  else
  {
    v10 = *(_QWORD *)(a1 + 104);
    if ( v10 == a1 )
      goto LABEL_12;
  }
  if ( v10 != 0 )
    return false;
LABEL_12:
  if ( (unsigned __int8)sub_14094B2D0(a1) != 0 )
    return false;
  v11 = *(char *)(a1 + 244);
  if ( (unsigned int)(v11 - 8) < 0x1F )
  {
    v12 = 2113929217;
    if ( _bittest(&v12, v11 - 8) )
      return false;
  }
  if ( ((v11 - 23) & 0xFFFFFFEF) == 0 )
    return false;
  if ( *(_QWORD *)(a1 + 96) == 0 )
  {
    if ( (_BYTE)v11 != 26 )
      goto LABEL_24;
    return false;
  }
  if ( (_BYTE)v11 != 29 )
  {
    if ( (unsigned __int8)v11 != 26 )
    {
      if ( (unsigned __int8)v11 != 14 )
        goto LABEL_24;
      goto LABEL_20;
    }
    return false;
  }
LABEL_20:
  result = false;
  if ( a5 == 0 || (_BYTE)v11 != 14 )
    return result;
LABEL_24:
  if ( (unsigned __int8)sub_140EBF780(a1) != 0 )
    return false;
  v14 = *(_QWORD *)(a1 + 176);
  if ( v14 == 0 && *(_BYTE *)(a1 + 244) == 0xFF )
    return false;
  if ( v14 != 0 && *(_WORD *)(v14 + 564) == 0xFFFA )
    return false;
  if ( (unsigned __int8)sub_140FCB830(a1) != 0 )
    return false;
  result = *(_DWORD *)(a1 + 12) != 98015063;
  if ( *(_DWORD *)(a1 + 12) != 98015063 && a4 == 0 )
  {
    v15 = *(_QWORD *)(a1 + 96);
    if ( v15 == 0 )
      return false;
    if ( *(_QWORD *)(v15 + 240) == 0 )
      return false;
    v16 = *(_QWORD *)(a1 + 88);
    if ( v16 == 0 )
      return false;
    if ( v16 != a3 )
      return false;
    result = true;
    if ( *(_QWORD *)(a3 + 96) == 0 )
      return false;
  }
  return result;
}
