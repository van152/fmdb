__int64 __fastcall sub_140EBAA10(__int64 a1, __int64 a2, __int64 a3)
{
  __int64 v4; // r14
  _QWORD *v5; // rcx
  __int64 v6; // rdx
  __int64 v7; // rcx
  __int64 *v8; // rax
  __int64 *v9; // rdx
  __int64 v10; // rbx
  __int64 v11; // rsi
  _QWORD *v12; // rdi
  __int64 v13; // r8
  _QWORD *v14; // rax
  _QWORD *v15; // rcx
  __int64 v16; // rcx
  __int64 v17; // rdx
  __int64 v18; // rax
  unsigned __int64 v19; // rcx
  unsigned __int64 v20; // rax
  __int64 v21; // rcx
  __int64 v22; // rcx
  __int64 v23; // rax
  unsigned __int64 v24; // rsi
  __int64 v25; // rcx
  __int64 v26; // rbx
  __int64 v27; // rax
  __int64 v28; // rax
  __int16 v29; // cx
  int v30; // edx
  int v31; // ecx
  int v32; // ebx
  int v33; // edi
  unsigned __int16 v34; // cx
  bool v35; // cc
  __int64 v36; // rax
  unsigned __int64 v37; // rcx
  __int64 v38; // rbx
  __int64 v39; // rdi
  bool v40; // al
  char v42; // r15
  __int128 v43; // [rsp+20h] [rbp-20h] BYREF
  __int64 v44; // [rsp+30h] [rbp-10h]
  __int64 v45; // [rsp+38h] [rbp-8h]

  v45 = -2;
  v4 = *(_QWORD *)(a1 + 168);
  v5 = *(_QWORD **)(a1 + 176);
  if ( v5 != nullptr )
  {
    if ( v5[36] == a1 )
      goto LABEL_15;
    v6 = v5[7];
    v7 = v5[8];
    v8 = nullptr;
    if ( v6 != v7 )
    {
      while ( *(_DWORD *)v6 != 1400071029 )
      {
        v6 += 16;
        if ( v6 == v7 )
          goto LABEL_10;
      }
      if ( v6 == v7 )
        v8 = nullptr;
      else
        v8 = *(__int64 **)(v6 + 8);
    }
LABEL_10:
    v9 = &qword_141B5A4A0;
    if ( v8 != nullptr )
      v9 = v8;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v9 + 48LL))(*v9) != 0 )
      return 0;
    v5 = *(_QWORD **)(a1 + 176);
    if ( v5 != nullptr && v5[36] == a1 )
    {
LABEL_15:
      if ( qword_141ABD470 == 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(&unk_141B59A68);
            sub_141751048(sub_1407E4B20);
            sub_141750EA0(&dword_141B59AA8);
          }
        }
        qword_141ABD470 = (__int64)&unk_141B59A68;
        v5 = *(_QWORD **)(a1 + 176);
      }
      v43 = 0;
      v44 = 0;
      LOBYTE(a3) = 1;
      sub_140988870(v5, &v43, a3);
      if ( *((_QWORD *)&v43 + 1) != (_QWORD)v43 )
      {
        v10 = (__int64)(*((_QWORD *)&v43 + 1) - v43) >> 3;
        do
        {
          v11 = v10--;
          v12 = *(_QWORD **)(a1 + 176);
          v13 = *(_QWORD *)(v43 + 8 * v11 - 8);
          v14 = (_QWORD *)v12[43];
          v15 = (_QWORD *)v12[44];
          if ( v14 == v15 )
          {
            v16 = v12[37];
            v17 = v12[38];
            if ( v16 != v17 && v12[36] != v13 && v12[40] != v12[41] )
            {
              v18 = sub_141751B70(v16, v17, v13);
              v19 = (unsigned __int64)(v18 - v12[37]) >> 3;
              if ( v18 == v12[38] )
                LODWORD(v19) = -1;
              if ( (v19 & 0x80000000) != 0LL
                || (v20 = (unsigned int)v19, v21 = v12[40], (v12[41] - v21) >> 3 <= v20)
                || *(_QWORD *)(v21 + 8 * v20) == 0 )
              {
LABEL_20:
                sub_141758A00();
                *((_QWORD *)&v43 + 1) -= 8LL;
              }
            }
          }
          else
          {
            while ( *v14 != v13 )
            {
              if ( ++v14 == v15 )
                goto LABEL_20;
            }
          }
        }
        while ( v10 != 0 );
      }
      v22 = *(_QWORD *)(a1 + 176);
      v23 = *(_QWORD *)(v22 + 296);
      if ( *(_QWORD *)(v22 + 304) != v23 )
      {
        v24 = 0;
        while ( 1 )
        {
          v26 = *(_QWORD *)(v23 + 8 * v24);
          if ( *(_QWORD *)(v26 + 168) != 0 )
          {
            v27 = sub_141751B70(v43, *((_QWORD *)&v43 + 1), *(_QWORD *)(v23 + 8 * v24));
            if ( v27 != *((_QWORD *)&v43 + 1) )
              break;
            if ( v27 == (_QWORD)v43 )
            {
              v36 = *(_QWORD *)(a1 + 168);
              if ( v36 != 0 && *(_WORD *)(*(_QWORD *)(v26 + 168) + 84LL) > *(_WORD *)(v36 + 84) )
              {
                v42 = 1;
                goto LABEL_64;
              }
            }
          }
LABEL_39:
          ++v24;
          v25 = *(_QWORD *)(a1 + 176);
          v23 = *(_QWORD *)(v25 + 296);
          if ( v24 >= (*(_QWORD *)(v25 + 304) - v23) >> 3 )
            goto LABEL_63;
        }
        v28 = *(_QWORD *)(v26 + 168);
        if ( v4 != 0 )
        {
          v29 = *(_WORD *)(v28 + 86);
          if ( *(_WORD *)(v4 + 86) != 0 )
          {
            if ( v29 == 0 )
              goto LABEL_39;
            goto LABEL_45;
          }
          if ( v29 == 0 )
          {
LABEL_45:
            v30 = HIWORD(*(_DWORD *)(v4 + 80));
            v31 = *(_DWORD *)(v4 + 80) & 0x1FF;
            if ( v30 == 1900 && (_WORD)v31 == 1
              || (v32 = HIWORD(*(_DWORD *)(v28 + 80)), v33 = *(_DWORD *)(v28 + 80) & 0x1FF, v32 == 1900)
              && (_WORD)v33 == 1
              || (_WORD)v30 == (_WORD)v32 && (_WORD)v31 == (_WORD)v33 )
            {
              v34 = *(_WORD *)(v28 + 84);
              v35 = *(_WORD *)(v4 + 84) < v34;
              if ( *(_WORD *)(v4 + 84) == v34 )
                v35 = *(_BYTE *)(v4 + 94) < *(_BYTE *)(v28 + 94);
              if ( !v35 )
                goto LABEL_39;
            }
            else if ( (unsigned __int16)v30 >= (unsigned __int16)v32
                   && ((unsigned __int16)v30 > (unsigned __int16)v32 || (unsigned __int16)v31 >= (unsigned __int16)v33) )
            {
              goto LABEL_39;
            }
          }
        }
        v4 = v28;
        goto LABEL_39;
      }
LABEL_63:
      v42 = 0;
LABEL_64:
      if ( (_QWORD)v43 != 0 )
      {
        v37 = v44 - v43;
        if ( v44 - (_QWORD)v43 == -1 )
        {
          v37 = *(unsigned int *)(v43 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_73:
            MEMORY[0x141948990](v43 - *(unsigned int *)(qword_141ABD470 + 48));
            goto LABEL_74;
          }
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_73;
        }
        v38 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v38) >> 3 <= v37 )
          goto LABEL_73;
        v39 = *(_QWORD *)(v38 + 8 * v37);
        if ( v39 == 0 )
          goto LABEL_73;
        MEMORY[0x1419475D8](v39 + 32, v43 - *(unsigned int *)(v39 + 120));
        v40 = *(_BYTE *)(v39 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 + 64)) != 0;
        if ( !v40 && *(_BYTE *)(v39 + 97) != 0 )
          sub_1412D33C0(v39);
      }
LABEL_74:
      if ( v42 != 0 )
        return 0;
    }
  }
  return v4;
}
