char __fastcall sub_1415D8DA0(__int64 a1, __int64 a2, _QWORD *a3)
{
  __int64 v3; // rax
  __int64 v4; // rsi
  char v5; // al
  char v6; // cl
  char v7; // cl
  char v8; // al
  char v9; // cl
  char v11; // al
  char v12; // cl
  char v13; // al
  char v14; // cl
  char v15; // al
  char v16; // cl
  __int64 v17; // r15
  __int64 v18; // rdi
  __int64 v19; // r14
  __int64 v20; // r13
  _QWORD *v21; // rbx
  _QWORD *v22; // rax
  _QWORD *v23; // rdi
  char v24; // al
  char v25; // cl
  __int64 v26; // r12
  _BYTE v27[64]; // [rsp+28h] [rbp-40h] BYREF

  v3 = -*(_DWORD *)(a1 - 4);
  v4 = a1 + v3;
  if ( (int)a2 <= 1248030306 )
  {
    if ( (int)a2 > 1248028012 )
    {
      switch ( (_DWORD)a2 )
      {
        case 0x4A63656D:
          v17 = a1 + v3 - 136;
          v18 = qword_141B5FDF0;
          sub_140FE7960(a1: v27, a2: a3, a3: 1298490451);
          v19 = sub_140FA3700(a1: v18, a2: v27);
          v20 = *(_QWORD *)(v4 - 24);
          if ( v20 != 0 )
          {
            v21 = *(_QWORD **)(v20 + 224);
            v22 = (_QWORD *)sub_141751B70(a1: *(_QWORD *)(v20 + 216), a2: v21, a3: v17);
            v23 = v22;
            if ( v22 != v21 )
            {
              while ( ++v22 != v21 )
              {
                if ( *v22 != v17 )
                  *v23++ = *v22;
              }
            }
            if ( v23 != v21 )
            {
              v26 = *(_QWORD *)(v20 + 224) - (_QWORD)v21;
              sub_141758A00(a1: v23, a2: v21, a3: v26);
              *(_QWORD *)(v20 + 224) = (char *)v23 + v26;
            }
          }
          *(_QWORD *)(v4 - 24) = v19;
          if ( v19 != 0 )
            sub_14154DDA0(a1: v19, a2: v17);
          return 1;
        case 0x4A636578:
          v24 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
          v25 = *(_BYTE *)(v4 - 15);
          if ( v24 != 0 )
            v7 = v25 | 2;
          else
            v7 = v25 & 0xFD;
          goto LABEL_48;
        case 0x4A636974:
          v8 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
          v9 = *(_BYTE *)(v4 - 15);
          if ( v8 != 0 )
            v7 = v9 | 0x20;
          else
            v7 = v9 & 0xDF;
          goto LABEL_48;
        default:
          break;
      }
    }
    else
    {
      switch ( (_DWORD)a2 )
      {
        case 0x4A63636E:
          v11 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
          v12 = *(_BYTE *)(v4 - 15);
          if ( v11 != 0 )
            v7 = v12 | 4;
          else
            v7 = v12 & 0xFB;
          goto LABEL_48;
        case 0x4A636468:
          v13 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
          v14 = *(_BYTE *)(v4 - 15);
          if ( v13 != 0 )
            v7 = v14 | 0x10;
          else
            v7 = v14 & 0xEF;
          goto LABEL_48;
        case 0x4A63646C:
          v5 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
          v6 = *(_BYTE *)(v4 - 15);
          if ( v5 != 0 )
            v7 = v6 | 0x40;
          else
            v7 = v6 & 0xBF;
LABEL_48:
          *(_BYTE *)(v4 - 15) = v7;
          return 1;
        default:
          break;
      }
    }
    return sub_140DFF760(a1: v4 - 16, a2, a3);
  }
  if ( (int)a2 > 1249079158 )
  {
    if ( (_DWORD)a2 != 1249079159 )
    {
      if ( (_DWORD)a2 == 1349742177 || (_DWORD)a2 == 1348890209 )
        *(_BYTE *)(v4 + 24) |= 0x10u;
      return sub_140DFF760(a1: v4 - 16, a2, a3);
    }
    *(_BYTE *)(v4 - 16) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
  }
  else
  {
    switch ( (_DWORD)a2 )
    {
      case 0x4A636E63:
        v15 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
        v16 = *(_BYTE *)(v4 - 15);
        if ( v15 != 0 )
          v7 = v16 | 8;
        else
          v7 = v16 & 0xF7;
        goto LABEL_48;
      case 0x4A637572:
        *(_BYTE *)(v4 - 13) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
        break;
      case 0x4A686F6E:
        *(_BYTE *)(v4 - 14) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
        break;
      default:
        return sub_140DFF760(a1: v4 - 16, a2, a3);
    }
  }
  return 1;
}
