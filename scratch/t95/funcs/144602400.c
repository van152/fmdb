__int64 __fastcall sub_144602400(__int64 a1, __int64 a2, char a3)
{
  __int64 result; // rax
  _BYTE *v4; // rcx
  __int64 i; // rdx
  _QWORD *v6; // r8
  __int64 v7; // r9
  int v8; // r9d

  result = a1;
  *(_QWORD *)(a1 + 6) = 0;
  *(_QWORD *)a1 = 0;
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 22) = 0;
  *(_QWORD *)(a1 + 32) = 0;
  *(_QWORD *)(a1 + 38) = 0;
  *(_QWORD *)(a1 + 48) = 0;
  *(_QWORD *)(a1 + 54) = 0;
  *(_QWORD *)(a1 + 64) = 0;
  *(_QWORD *)(a1 + 70) = 0;
  *(_QWORD *)(a1 + 80) = 0;
  *(_QWORD *)(a1 + 86) = 0;
  *(_QWORD *)(a1 + 96) = 0;
  *(_QWORD *)(a1 + 102) = 0;
  *(_QWORD *)(a1 + 118) = 0;
  *(_QWORD *)(a1 + 112) = 0;
  *(_QWORD *)(a1 + 134) = 0;
  *(_QWORD *)(a1 + 128) = 0;
  *(_QWORD *)(a1 + 150) = 0;
  *(_QWORD *)(a1 + 144) = 0;
  *(_QWORD *)(a1 + 166) = 0;
  *(_QWORD *)(a1 + 160) = 0;
  *(_QWORD *)(a1 + 182) = 0;
  *(_QWORD *)(a1 + 176) = 0;
  *(_QWORD *)(a1 + 198) = 0;
  *(_QWORD *)(a1 + 192) = 0;
  *(_QWORD *)(a1 + 214) = 0;
  *(_QWORD *)(a1 + 208) = 0;
  *(_QWORD *)(a1 + 230) = 0;
  *(_QWORD *)(a1 + 224) = 0;
  *(_QWORD *)(a1 + 246) = 0;
  *(_QWORD *)(a1 + 240) = 0;
  *(_QWORD *)(a1 + 262) = 0;
  *(_QWORD *)(a1 + 256) = 0;
  *(_QWORD *)(a1 + 278) = 0;
  *(_QWORD *)(a1 + 272) = 0;
  *(_QWORD *)(a1 + 294) = 0;
  *(_QWORD *)(a1 + 288) = 0;
  *(_QWORD *)(a1 + 310) = 0;
  *(_QWORD *)(a1 + 304) = 0;
  *(_QWORD *)(a1 + 320) = a2;
  *(_BYTE *)(a1 + 328) = a3;
  v4 = (_BYTE *)(a1 + 13);
  for ( i = 0; i != 20; ++i )
  {
    *(v4 - 1) = i;
    if ( a3 != 0 )
    {
      if ( a3 == 1 )
      {
        v6 = *(_QWORD **)(result + 320);
        v7 = v6[135];
        if ( v7 != 0 )
          goto LABEL_3;
      }
      else
      {
        if ( a3 != 2 )
        {
          v6 = *(_QWORD **)(result + 320);
          v8 = 0;
          goto LABEL_4;
        }
        v6 = *(_QWORD **)(result + 320);
        v7 = v6[137];
        if ( v7 != 0 )
          goto LABEL_3;
      }
    }
    else
    {
      v6 = *(_QWORD **)(result + 320);
      v7 = v6[136];
      if ( v7 != 0 )
      {
LABEL_3:
        v8 = *(_DWORD *)(v7 + 4 * i);
        goto LABEL_4;
      }
    }
    v8 = 0;
LABEL_4:
    *(_DWORD *)(v4 - 5) = v8;
    *(_QWORD *)(v4 - 13) = v6;
    a3 = *(_BYTE *)(result + 328);
    *v4 = a3;
    v4 += 16;
  }
  return result;
}
