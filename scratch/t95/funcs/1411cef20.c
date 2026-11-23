char __fastcall sub_1411CEF20(__int64 a1)
{
  __int64 v1; // rdx
  __int64 *v2; // rax
  __int64 v3; // rax
  __int64 v4; // rdx
  unsigned __int8 v5; // r8
  char v6; // dl
  char result; // al
  char v8; // cl
  int v9; // edx

  v1 = *(_QWORD *)(a1 + 48);
  v2 = (__int64 *)(v1 + 368);
  if ( *(_BYTE *)(a1 + 47) == 0 )
    v2 = (__int64 *)(v1 + 216);
  v3 = *v2;
  if ( v3 != 0 && (*(_BYTE *)(v1 + 185) != 0 && (v4 = *(_QWORD *)(v3 + 272)) != 0 || (v4 = *(_QWORD *)(v3 + 264)) != 0) )
  {
    v5 = *(_BYTE *)(v4 + 1956);
    if ( *(char *)(a1 + 44) <= 0 || *(_BYTE *)(a1 + 44) == 100 )
    {
      v6 = 21;
      if ( (unsigned int)(*(_DWORD *)(a1 + 12) - 562397) >= 2 )
      {
        v6 = 23;
        switch ( *(_BYTE *)(a1 + 40) )
        {
          case 9:
          case 0x2B:
            break;
          case 0xA:
          case 0x15:
            v6 = 21;
            break;
          case 0xB:
          case 0x24:
            v6 = 19;
            break;
          case 0xC:
          case 0x25:
            v6 = 18;
            break;
          case 0x12:
            v6 = 20;
            break;
          case 0x1D:
            v6 = 17;
            break;
          case 0x21:
            v6 = 22;
            break;
          default:
            v6 = 100;
            break;
        }
      }
      *(_BYTE *)(a1 + 44) = v6;
    }
    return *(_BYTE *)(a1 + 44) > 0 && *(_BYTE *)(a1 + 44) <= v5;
  }
  else
  {
    v8 = *(_BYTE *)(a1 + 40);
    if ( (unsigned __int8)(v8 - 10) >= 0x1Cu )
      return v8 == 9 || v8 == 43;
    result = 1;
    v9 = 209717511;
    if ( !_bittest(&v9, (unsigned __int8)(v8 - 10)) )
      return v8 == 9 || v8 == 43;
  }
  return result;
}
