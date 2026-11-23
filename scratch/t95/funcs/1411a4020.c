char __fastcall sub_1411A4020(__int64 a1, __int64 a2)
{
  bool v3; // zf
  _QWORD *v4; // rcx
  __int64 *v5; // rbx
  __int64 *v6; // r10
  int v7; // r8d
  __int64 v8; // r9
  __int64 **v9; // rsi
  __int64 *v10; // rax
  unsigned int v11; // edi
  int v12; // eax
  __int64 v13; // rax
  _QWORD *v14; // rax
  _QWORD *v15; // rcx
  unsigned int v16; // ecx

  v3 = *(_BYTE *)(a1 + 47) == 0;
  v4 = *(_QWORD **)(a1 + 48);
  if ( !v3 || v4 == nullptr )
    goto LABEL_18;
  v5 = (__int64 *)v4[35];
  v6 = (__int64 *)v4[36];
  if ( v5 == v6 )
  {
    if ( a2 == 0 )
      goto LABEL_13;
LABEL_18:
    if ( v4 == (_QWORD *)a2 )
    {
      v14 = *(_QWORD **)(a2 + 24);
      if ( v14 == *(_QWORD **)(a2 + 32) )
        goto LABEL_27;
      goto LABEL_24;
    }
    v14 = (_QWORD *)v4[3];
    v15 = (_QWORD *)v4[4];
    if ( v14 == v15 )
      goto LABEL_27;
    if ( *v14 != a1 )
    {
      if ( v14 != v15 )
      {
LABEL_24:
        if ( *v14 == a1 )
        {
          v16 = (char)sub_1411CC0E0(a1, a2) - 18;
          if ( v16 < 6 )
            return 0x9210A120B0CuLL >> (8 * (unsigned __int8)v16);
        }
      }
LABEL_27:
      LOBYTE(v13) = *(_BYTE *)(a1 + 40);
      return v13;
    }
LABEL_35:
    LOBYTE(v13) = -1;
    return v13;
  }
  v7 = 1049072;
  v8 = 0;
  v9 = (__int64 **)v4[35];
  while ( 1 )
  {
    v10 = *v9;
    if ( (_QWORD *)(*v9)[1] == v4 )
    {
      v11 = *((unsigned __int8 *)v10 + 48);
      if ( v11 <= 0x14 )
      {
        if ( _bittest(&v7, v11) )
          break;
      }
    }
    if ( ++v9 == (__int64 **)v6 )
      goto LABEL_10;
  }
  v8 = *v10;
LABEL_10:
  if ( v8 != a2 )
    goto LABEL_18;
LABEL_13:
  v12 = *(char *)(a1 + 40);
  if ( *(_BYTE *)(a1 + 40) != 0 )
  {
    switch ( v12 )
    {
      case 9:
        LOBYTE(v13) = 43;
        return v13;
      case 12:
        LOBYTE(v13) = 37;
        return v13;
      case 11:
        LOBYTE(v13) = 36;
        return v13;
      default:
        break;
    }
    goto LABEL_18;
  }
  if ( v5 == v6 )
    goto LABEL_35;
  while ( *(_QWORD **)(*v5 + 8) != v4 )
  {
LABEL_31:
    if ( ++v5 == v6 )
      goto LABEL_35;
  }
  LOBYTE(v13) = 3;
  switch ( *(_BYTE *)(*v5 + 48) )
  {
    case 4:
      return v13;
    case 5:
      LOBYTE(v13) = 13;
      break;
    case 6:
      LOBYTE(v13) = 16;
      break;
    case 7:
      LOBYTE(v13) = 17;
      break;
    case 8:
      LOBYTE(v13) = 15;
      break;
    case 0x14:
      LOBYTE(v13) = 30;
      break;
    default:
      goto LABEL_31;
  }
  return v13;
}
