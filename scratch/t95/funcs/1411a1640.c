char __fastcall sub_1411A1640(__int64 a1, char a2, __int64 a3, char a4, unsigned __int8 a5)
{
  int v8; // edx
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rax
  __int64 v13; // rsi
  __int64 v14; // r15
  char v15; // cl
  __int64 v16; // rax
  __int64 *v17; // rbp
  __int64 v18; // rdx
  __int64 v19; // rax
  int v20; // ecx
  __int64 *v21; // rbx
  __int64 *v22; // rsi
  char v23; // r13
  int v24; // ecx
  __int64 v25; // rax
  __int64 v26; // rax
  __int64 v27; // rcx
  __int64 v28; // rax
  unsigned __int64 v29; // rcx
  __int64 *v30; // rbp
  __int64 v31; // rdx
  __int64 v32; // rbp
  _QWORD *v33; // rsi
  _QWORD *v34; // rax
  _QWORD *v35; // rdi
  __int64 v36; // rbx
  _QWORD v38[9]; // [rsp+30h] [rbp-48h] BYREF

  if ( a2 == 0 )
  {
LABEL_4:
    if ( a4 == 0 )
      return 1;
    goto LABEL_5;
  }
  v8 = a1 + 48;
  if ( *(_BYTE *)(a1 + 47) != 0 )
  {
    sub_140F7EC80(a3, v8, *(_QWORD *)(a3 + 96), a5, 1, 0);
    goto LABEL_4;
  }
  sub_140F7EE40(a3, v8, *(_QWORD *)(a3 + 16), a5, 1, 0);
  if ( a4 == 0 )
    return 1;
LABEL_5:
  sub_140F7EC80(a3, a1 + 96, *(_QWORD *)(a3 + 24), a5, 1, 0);
  if ( *(_BYTE *)(a1 + 47) != 0 || (v9 = *(_QWORD *)(a1 + 48)) == 0 || *(_QWORD *)(v9 + 216) != 0 )
  {
    sub_140F7EC80(a3, a1 + 88, *(_QWORD *)(a3 + 24), a5, 1, 0);
    sub_140F7EC80(a3, a1 + 80, *(_QWORD *)(a3 + 24), a5, 1, 0);
    sub_140F7EC80(a3, a1 + 104, *(_QWORD *)(a3 + 24), a5, 1, 0);
    sub_140F7EC80(a3, a1 + 112, *(_QWORD *)(a3 + 24), a5, 1, 0);
  }
  else
  {
    *(_QWORD *)(a1 + 88) = 0;
    *(_QWORD *)(a1 + 80) = 0;
    *(_QWORD *)(a1 + 104) = 0;
    *(_QWORD *)(a1 + 112) = 0;
  }
  sub_140F7FD40(a3, a1 + 120, a5);
  if ( (a5 & 8) != 0 )
  {
    v11 = *(_QWORD *)(a1 + 128);
    if ( v11 != 0 )
      v10 = v11 + *(int *)(*(_QWORD *)(v11 + 8) + 4LL) + 8;
    else
      v10 = 0;
  }
  else
  {
    v10 = *(_QWORD *)(a1 + 128);
  }
  v38[0] = v10;
  if ( (unsigned __int8)sub_140F80250(a3, v38, a5, 0) != 0 )
  {
    if ( v38[0] != 0 )
      v12 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v38[0] + 1688LL))(v38[0]);
    else
      v12 = 0;
    *(_QWORD *)(a1 + 128) = v12;
  }
  sub_140F7EC80(a3, a1 + 152, *(_QWORD *)(a3 + 24), a5, 1, 0);
  v13 = a1 + 136;
  sub_140F80250(a3, a1 + 136, a5, 0);
  v14 = a1 + 144;
  sub_140F80250(a3, a1 + 144, a5, 0);
  v15 = *(_BYTE *)(a1 + 47);
  v16 = *(_QWORD *)(a1 + 48);
  v17 = (__int64 *)(v16 + 216);
  if ( v15 != 0 )
    v17 = (__int64 *)(v16 + 368);
  v18 = *v17;
  if ( *v17 != 0 )
  {
    if ( *(_BYTE *)(v16 + 185) == 0 || (v19 = *(_QWORD *)(v18 + 272)) == 0 )
      v19 = *(_QWORD *)(v18 + 264);
    if ( v19 != 0 && v15 == 1 && *(_BYTE *)(qword_141B5FE10 + 89) != 0 )
    {
      v20 = *(_DWORD *)(*(_QWORD *)(v19 + 368) + 12LL);
      if ( v20 == 215446 || v20 == 791 )
      {
        *(_QWORD *)(a1 + 144) = 0;
        *(_QWORD *)v13 = 0;
      }
      else if ( (*(_BYTE *)(v19 + 1150) & 2) != 0 && (unsigned __int8)sub_1400015E0() != 0 )
      {
        if ( *(_QWORD *)v13 != 0 && (*(_BYTE *)(*(_QWORD *)v13 + 24LL) & 8) == 0 )
          *(_QWORD *)v13 = 0;
        if ( *(_QWORD *)v14 != 0 && (*(_BYTE *)(*(_QWORD *)v14 + 24LL) & 8) == 0 )
          *(_QWORD *)v14 = 0;
      }
    }
  }
  v21 = *(__int64 **)(a1 + 56);
  v22 = *(__int64 **)(a1 + 64);
  if ( v21 != v22 )
  {
    v23 = 0;
    do
    {
      if ( (a5 & 8) != 0 )
      {
        if ( *v21 != 0 )
          v25 = *v21 + *(int *)(*(_QWORD *)(*v21 + 8) + 4LL) + 8;
        else
          v25 = 0;
      }
      else
      {
        v25 = *v21;
      }
      v38[0] = v25;
      if ( (unsigned __int8)sub_140F80250(a3, v38, a5, 0) != 0 )
      {
        v26 = v38[0] != 0 ? (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v38[0] + 1672LL))(v38[0]) : 0LL;
        *v21 = v26;
        v23 = 1;
        if ( *v21 != 0 )
        {
          v27 = *v21 + *(int *)(*(_QWORD *)(*v21 + 8) + 4LL) + 8;
          v28 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v27 + 1832LL))(v27);
          if ( v28 != 0 )
          {
            if ( *(unsigned __int16 *)(a3 + 1416) <= 0xDD6u )
              *(_BYTE *)(v28 + 31) |= 0x80u;
            v29 = *(unsigned int *)(v28 + 16);
            if ( (v29 & 0x80000000) == 0LL )
            {
              if ( (_BYTE)word_141B60320 != 0 )
              {
                v30 = *(__int64 **)(qword_141B5FE40 + 128);
                v31 = *v30;
                v32 = v30[1];
              }
              else
              {
                v31 = *(_QWORD *)(qword_141B5FE40 + 96);
                v32 = *(_QWORD *)(qword_141B5FE40 + 104);
              }
              if ( (v32 - v31) >> 3 > v29 && (unsigned int)*(_QWORD *)(v31 + 8 * v29) == -1 )
              {
                if ( *(_DWORD *)(a1 + 8) != 0 )
                  v24 = *(_DWORD *)(*(int *)(a1 + 8) + 8LL);
                else
                  v24 = -1;
                *(_DWORD *)(v28 + 16) = v24;
              }
            }
          }
        }
      }
      ++v21;
    }
    while ( v21 != v22 );
    if ( (v23 & 1) != 0 )
    {
      v33 = *(_QWORD **)(a1 + 64);
      v34 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 56), v33, 0);
      v35 = v34;
      if ( v34 != v33 )
      {
        while ( ++v34 != v33 )
        {
          if ( *v34 != 0 )
            *v35++ = *v34;
        }
      }
      if ( v35 != v33 )
      {
        v36 = *(_QWORD *)(a1 + 64) - (_QWORD)v33;
        sub_141758A00(v35, v33, v36);
        *(_QWORD *)(a1 + 64) = (char *)v35 + v36;
      }
    }
  }
  return 1;
}
