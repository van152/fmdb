__int64 __fastcall sub_1411F4C60(__int64 *a1, unsigned __int8 a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  unsigned __int64 v6; // rcx
  __int64 v7; // rax
  int v8; // edi
  int v9; // esi
  int v10; // r15d
  __int64 *v11; // rdx
  __int64 v12; // rax
  __int64 v13; // rbx
  char v14; // al
  unsigned int v15; // eax
  int v16; // edx
  unsigned int v17; // ecx
  __int64 v18; // rax
  int v19; // esi
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rsi
  __int64 v24[3]; // [rsp+28h] [rbp-28h] BYREF
  __int64 v25; // [rsp+40h] [rbp-10h] BYREF
  int v26; // [rsp+48h] [rbp-8h]
  __int64 v27; // [rsp+50h] [rbp+0h]

  v27 = -2;
  sub_1407C9510(v24);
  v5 = sub_14083D4F0(v4);
  v26 = (char)a2;
  v25 = v5 + 40;
  sub_140833EB0(v24, 1417040752, &v25);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
  v6 = (unsigned int)a2 - 2;
  v7 = *a1;
  v8 = 1500;
  v9 = 300;
  v10 = 3000;
  switch ( a2 )
  {
    case 2u:
      goto LABEL_4;
    case 3u:
      v8 = 4500;
      v9 = 600;
      v10 = 6000;
      goto LABEL_4;
    case 4u:
      v8 = 7000;
      v9 = 1500;
      v10 = 9000;
LABEL_4:
      v6 = *(_QWORD *)(v7 + 48);
      v11 = (__int64 *)(v6 + 368);
      if ( *(_BYTE *)(v7 + 47) == 0 )
        v11 = (__int64 *)(v6 + 216);
      v12 = *v11;
      if ( *v11 != 0
        && (*(_BYTE *)(v6 + 185) != 0 && (v13 = *(_QWORD *)(v12 + 272)) != 0 || (v13 = *(_QWORD *)(v12 + 264)) != 0) )
      {
        v14 = sub_141758D10();
        if ( v14 < 2 )
          v14 = 1;
        v15 = (unsigned int)(unsigned __int8)v14 * v8 / 0xA;
        v16 = *(_DWORD *)(*(_QWORD *)(v13 + 368) + 452LL) / 1000000;
        if ( v16 < 2 )
          v16 = 1;
        v17 = 100;
        if ( v16 < 100 )
          v17 = v16;
        v6 = v15 * (v17 >> 1);
        if ( (int)(v6 / 0x32) > v9 )
          v9 = v6 / 0x32;
        if ( v9 >= v10 )
          v9 = v10;
        v8 = v9;
      }
      break;
    case 5u:
      v8 = 10000;
      break;
    case 6u:
      v8 = 20000;
      break;
    case 7u:
      v8 = 30000;
      break;
    default:
      v8 = 0;
      break;
  }
  v18 = sub_14083D4F0(v6);
  v26 = v8;
  v25 = v18 + 40;
  sub_140833EB0(v24, 1417048899, &v25);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
  v19 = *(_DWORD *)(a1[1] + 736);
  v21 = sub_14083D4F0(v20);
  LOBYTE(v26) = v8 <= v19;
  v25 = v21 + 24;
  sub_140833EB0(v24, 1417048897, &v25);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
  v22 = a1[2];
  sub_14083DDA0(&v25, v24);
  sub_14083B5F0(v22, &v25);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
  return sub_140833970(v24);
}
