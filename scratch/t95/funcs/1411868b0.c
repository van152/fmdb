char __fastcall sub_1411868B0(__int64 a1, int a2, __int64 *a3)
{
  __int64 v6; // rcx
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rcx
  __int16 v11; // ax
  __int64 v12; // rcx
  __int16 v13; // ax
  float v14; // xmm6_4
  __int64 v15; // rax
  char v16; // al
  __int64 v17; // rcx
  __int16 v18; // si
  int v19; // esi
  __int64 v20; // rcx
  float v21; // xmm6_4
  __int64 v22; // rcx
  __int64 v23; // rax
  char v24; // si
  float v25; // xmm6_4
  __int16 v26; // ax
  __int64 v27; // rax
  __int64 v28; // rax
  __int64 v29; // rax
  __int64 v30; // rax
  __int64 *v31; // rdi
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rax
  __int64 v35; // rcx
  __int64 v36; // rcx
  __int64 v37; // rcx
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 v40; // rax
  __int64 v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rax
  __int64 v44; // r13
  __int64 v45; // rdi
  __int64 v46; // r14
  __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rax
  __int64 v50; // rax
  __int64 v51; // rcx
  __int64 v52; // rax
  float v53; // xmm6_4
  __int64 v54; // rcx
  __int64 v55; // rax
  _QWORD v56[2]; // [rsp+20h] [rbp-60h] BYREF
  __int64 v57; // [rsp+30h] [rbp-50h] BYREF
  __int64 v58; // [rsp+38h] [rbp-48h] BYREF
  __int64 *v59; // [rsp+48h] [rbp-38h]
  __int128 v60; // [rsp+50h] [rbp-30h] BYREF
  __int64 v61; // [rsp+60h] [rbp-20h]
  __int64 v62; // [rsp+70h] [rbp-10h] BYREF
  _QWORD v63[3]; // [rsp+78h] [rbp-8h] BYREF

  v63[2] = -2;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5F3E8 + 32LL))(qword_141B5F3E8) == 0
    && (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, __int64 *))(*(_QWORD *)qword_141B5F3E8 + 48LL))(
         qword_141B5F3E8,
         a1,
         (unsigned int)a2,
         a3) != 0 )
  {
    return 1;
  }
  if ( a2 <= 1399743862 )
  {
    if ( a2 > 1399087992 )
    {
      if ( a2 > 1399611763 )
      {
        if ( a2 <= 1399683179 )
        {
          if ( a2 <= 1399680619 )
          {
            if ( a2 == 1399611764 )
            {
              LODWORD(v63[0]) = *(_DWORD *)(a1 + 96);
              v62 = sub_14083D4F0(v6) + 104;
              sub_14083DFA0(a3, &v62);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
              return 1;
            }
            if ( a2 == 1399615342 )
            {
              LODWORD(v63[0]) = *(_DWORD *)(a1 + 100);
              v62 = sub_14083D4F0(v6) + 104;
              sub_14083DFA0(a3, &v62);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
              return 1;
            }
            return sub_140FE3F20((_DWORD *)a1, a2, a3);
          }
          if ( a2 == 1399680620 )
          {
            v25 = (float)*(__int16 *)(a1 + 144) / MEMORY[0x141775530];
            if ( v25 > MEMORY[0x141759000] )
              goto LABEL_204;
          }
          else
          {
            if ( a2 != 1399680631 )
              return sub_140FE3F20((_DWORD *)a1, a2, a3);
            v25 = (float)*(__int16 *)(a1 + 146) / MEMORY[0x141775530];
            if ( v25 > MEMORY[0x141759000] )
              goto LABEL_204;
          }
        }
        else
        {
          if ( a2 > 1399742828 )
          {
            if ( a2 == 1399742829 )
            {
              v31 = (__int64 *)(a1 + 56);
              v32 = sub_14083D4F0(v6);
              v63[0] = 0;
              if ( v63 != v31 )
              {
                v33 = *v31;
                if ( *v31 != 0 )
                  _InterlockedIncrement((volatile signed __int32 *)(v33 - 4));
                v63[0] = v33;
              }
              v62 = v32 + 136;
              sub_14083DFA0(a3, &v62);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
              return 1;
            }
            if ( a2 != 1399742836 )
            {
              if ( a2 == 1399743091 )
              {
                sub_140FE77A0(*(_QWORD *)(a1 + 88), a3);
                return 1;
              }
              return sub_140FE3F20((_DWORD *)a1, a2, a3);
            }
            v34 = *(_QWORD *)(a1 + 80);
            if ( v34 == 0 )
              return 1;
            v35 = *(_QWORD *)(v34 + 32);
            if ( v35 == 0 )
              return 1;
LABEL_157:
            sub_140FE7190(v35, &v62);
            sub_140FEAD00(&v62, &v60);
            sub_14083DFA0(a3, &v60);
            (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v63[0] + 16LL))(v63[0], v63);
            return 1;
          }
          if ( a2 == 1399683180 )
          {
            v25 = (float)*(__int16 *)(a1 + 148) / MEMORY[0x141775530];
            if ( v25 > MEMORY[0x141759000] )
              goto LABEL_204;
          }
          else
          {
            if ( a2 != 1399683191 )
              return sub_140FE3F20((_DWORD *)a1, a2, a3);
            v25 = (float)*(__int16 *)(a1 + 150) / MEMORY[0x141775530];
            if ( v25 > MEMORY[0x141759000] )
            {
LABEL_204:
              *(float *)v63 = v25;
              v62 = sub_14083D4F0(v6) + 104;
              sub_14083DFA0(a3, &v62);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
              return 1;
            }
          }
        }
LABEL_205:
        if ( a3 != &qword_141B5A4A0 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            a3);
        }
        return 1;
      }
      if ( a2 <= 1399156341 )
      {
        if ( a2 > 1399092337 )
        {
          if ( a2 == 1399092338 )
          {
            LODWORD(v63[0]) = *(char *)(a1 + 156);
            v62 = sub_14083D4F0(v6) + 40;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          if ( a2 == 1399153529 )
          {
            LODWORD(v63[0]) = *(_DWORD *)(a1 + 124);
            v62 = sub_14083D4F0(v6) + 40;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        if ( a2 == 1399087993 )
        {
          LODWORD(v63[0]) = *(char *)(a1 + 154);
          v62 = sub_14083D4F0(v6) + 40;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        if ( a2 != 1399089517 )
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        sub_1407C9510(&v62);
        v9 = sub_140FE8230();
        if ( v9 != 0 && *(_BYTE *)(v9 + 47) == 1 )
        {
          v11 = *(_WORD *)(a1 + 140);
          if ( v11 <= 0 )
            v11 = *(_WORD *)(a1 + 136);
          *((float *)&v60 + 2) = (float)v11 / MEMORY[0x141775530];
          *(_QWORD *)&v60 = sub_14083D4F0(v10) + 104;
          sub_140833EB0(&v62, 1818719336, &v60);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
          v13 = *(_WORD *)(a1 + 142);
          if ( v13 <= 0 )
            v13 = *(_WORD *)(a1 + 138);
          v14 = (float)v13 / MEMORY[0x141775530];
          v15 = sub_14083D4F0(v12);
          *((float *)&v60 + 2) = v14;
          *(_QWORD *)&v60 = v15 + 104;
          sub_140833EB0(&v62, 2003395700, &v60);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
        }
        else
        {
          *((float *)&v60 + 2) = (float)*(__int16 *)(a1 + 136) / MEMORY[0x141775530];
          *(_QWORD *)&v60 = sub_14083D4F0(v10) + 104;
          sub_140833EB0(&v62, 1818719336, &v60);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
          v53 = (float)*(__int16 *)(a1 + 138) / MEMORY[0x141775530];
          v55 = sub_14083D4F0(v54);
          *((float *)&v60 + 2) = v53;
          *(_QWORD *)&v60 = v55 + 104;
          sub_140833EB0(&v62, 2003395700, &v60);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
        }
        sub_14083DDA0(&v60, &v62);
        sub_14083DFA0(a3, &v60);
        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
LABEL_226:
        sub_140833970(&v62);
        return 1;
      }
      if ( a2 <= 1399420006 )
      {
        if ( a2 == 1399156342 )
        {
          LODWORD(v63[0]) = *(char *)(a1 + 160);
          v62 = sub_14083D4F0(v6) + 40;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        if ( a2 == 1399158900 )
        {
          LOBYTE(v63[0]) = *(_BYTE *)(a1 + 155) & 1;
          v62 = sub_14083D4F0(v6) + 24;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      if ( a2 == 1399420007 )
      {
        LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 155) & 4) != 0;
        v62 = sub_14083D4F0(v6) + 24;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      if ( a2 != 1399605581 )
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      v26 = *(_WORD *)(a1 + 140);
      if ( v26 <= 0 )
        goto LABEL_205;
LABEL_222:
      *(float *)v63 = (float)v26 / MEMORY[0x141775530];
      v62 = sub_14083D4F0(v6) + 104;
      sub_14083DFA0(a3, &v62);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
      return 1;
    }
    if ( a2 > 1399021938 )
    {
      if ( a2 > 1399026760 )
      {
        if ( a2 > 1399026792 )
        {
          if ( a2 == 1399026793 )
          {
            sub_140FE76A0(*(_QWORD *)(a1 + 80), a3);
            return 1;
          }
          if ( a2 == 1399087464 )
          {
            LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 155) & 0x40) != 0;
            v62 = sub_14083D4F0(v6) + 24;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        if ( a2 != 1399026761 )
        {
          if ( a2 == 1399026775 )
            return 1;
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        v35 = *(_QWORD *)(a1 + 80);
        if ( v35 == 0 )
          return 1;
        goto LABEL_157;
      }
      if ( a2 > 1399025762 )
      {
        if ( a2 == 1399025763 )
        {
          sub_1415E6D60(&v62, a1);
          sub_140E96790(&v62, a3);
          if ( v62 != 0 )
            sub_1407E4890(qword_141ABD470, v62, v63[1] - v62);
          return 1;
        }
        if ( a2 == 1399025785 )
        {
          LODWORD(v63[0]) = *(_DWORD *)(a1 + 108);
          v62 = sub_14083D4F0(v6) + 40;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      if ( a2 != 1399021939 )
      {
        if ( a2 == 1399025526 )
        {
          v16 = sub_140087040();
          v18 = *(_WORD *)(a1 + 166);
          if ( v16 != 0 && (v18 & 0x40) != 0 )
          {
            LOBYTE(v63[0]) = 1;
            v62 = sub_14083D4F0(v17) + 24;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          }
          else
          {
            LOBYTE(v63[0]) = v18 & 1;
            v62 = sub_14083D4F0(v17) + 24;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          }
          return 1;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      v19 = *(_DWORD *)(a1 + 120);
      if ( v19 <= 0 )
        goto LABEL_205;
    }
    else
    {
      if ( a2 <= 1316316005 )
      {
        if ( a2 > 1145392196 )
        {
          if ( a2 == 1145392197 )
          {
            LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 166) & 0x20) != 0;
            v62 = sub_14083D4F0(v6) + 24;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          if ( a2 == 1148150639 )
          {
            v27 = sub_140DBC940();
            LODWORD(v63[0]) = ((*(_WORD *)(a1 + 48) & 0x1FF) << 8)
                            | (*(unsigned __int16 *)(a1 + 48) >> 9)
                            | (*(unsigned __int16 *)(a1 + 50) << 17);
            v62 = v27;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
        }
        else if ( a2 == 1131701802 || a2 == 1131701875 )
        {
          v8 = sub_140FE84D0();
          if ( v8 != 0 )
            sub_140E8A400(v8, (__int64 *)(unsigned int)a2, a3);
          return 1;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      if ( a2 <= 1398957176 )
      {
        if ( a2 == 1316316006 )
        {
          LOBYTE(v63[0]) = *(_BYTE *)(a1 + 166) >> 7;
          v62 = sub_14083D4F0(v6) + 24;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        if ( a2 != 1397580905 )
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        sub_1407C9510(&v62);
        *((float *)&v60 + 2) = (float)*(__int16 *)(a1 + 148) / MEMORY[0x141775530];
        *(_QWORD *)&v60 = sub_14083D4F0(v20) + 104;
        sub_140833EB0(&v62, 1818719336, &v60);
        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
        v21 = (float)*(__int16 *)(a1 + 150) / MEMORY[0x141775530];
        v23 = sub_14083D4F0(v22);
        *((float *)&v60 + 2) = v21;
        *(_QWORD *)&v60 = v23 + 104;
        sub_140833EB0(&v62, 2003395700, &v60);
        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
        sub_14083DDA0(&v60, &v62);
        sub_14083DFA0(a3, &v60);
        (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
        goto LABEL_226;
      }
      if ( a2 != 1398957177 )
      {
        if ( a2 == 1398959204 )
        {
          v28 = sub_140DBC940();
          LODWORD(v63[0]) = ((*(_WORD *)(a1 + 40) & 0x1FF) << 8)
                          | (*(unsigned __int16 *)(a1 + 40) >> 9)
                          | (*(unsigned __int16 *)(a1 + 42) << 17);
          v62 = v28;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      v6 = *(_WORD *)(a1 + 40) & 0x1FF;
      v19 = 0;
      if ( (_WORD)v6 != 1 )
        v19 = *(unsigned __int16 *)(a1 + 42);
      if ( *(_WORD *)(a1 + 42) != 1900 )
        v19 = *(unsigned __int16 *)(a1 + 42);
    }
LABEL_212:
    LODWORD(v63[0]) = v19;
    v62 = sub_14083D4F0(v6) + 40;
    sub_14083DFA0(a3, &v62);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
    return 1;
  }
  if ( a2 <= 1400005240 )
  {
    if ( a2 > 1399876717 )
    {
      if ( a2 > 1399878754 )
      {
        if ( a2 <= 1399879523 )
        {
          if ( a2 == 1399878755 )
          {
            LODWORD(v63[0]) = *(__int16 *)(a1 + 152);
            v62 = sub_14083D4F0(v6) + 40;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          if ( a2 == 1399878777 )
          {
            v24 = 1;
            if ( *(_BYTE *)(a1 + 157) >= 2u )
              v24 = *(_BYTE *)(a1 + 157);
            LODWORD(v63[0]) = v24;
            v62 = sub_14083D4F0(v6) + 40;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        if ( a2 != 1399879524 )
        {
          if ( a2 == 1400005220 )
          {
            v30 = sub_140DBC940();
            LODWORD(v63[0]) = ((*(_WORD *)(a1 + 44) & 0x1FF) << 8)
                            | (*(unsigned __int16 *)(a1 + 44) >> 9)
                            | (*(unsigned __int16 *)(a1 + 46) << 17);
            v62 = v30;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        v52 = sub_140FE8230();
        if ( v52 == 0 || *(_BYTE *)(v52 + 47) != 1 )
        {
          *(float *)v63 = (float)*(__int16 *)(a1 + 138) / MEMORY[0x141775530];
          v62 = sub_14083D4F0(v6) + 104;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        v26 = *(_WORD *)(a1 + 142);
        if ( v26 <= 0 )
          v26 = *(_WORD *)(a1 + 138);
      }
      else
      {
        if ( a2 > 1399878251 )
        {
          if ( a2 == 1399878252 )
          {
            v50 = sub_140DBC940();
            LODWORD(v63[0]) = ((*(_WORD *)(a1 + 36) & 0x1FF) << 8)
                            | (*(unsigned __int16 *)(a1 + 36) >> 9)
                            | (*(unsigned __int16 *)(a1 + 38) << 17);
            v62 = v50;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          if ( a2 == 1399878258 )
          {
            LODWORD(v63[0]) = *(char *)(a1 + 158);
            v62 = sub_14083D4F0(v6) + 40;
            sub_14083DFA0(a3, &v62);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
            return 1;
          }
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        if ( a2 != 1399876718 )
        {
          if ( a2 == 1399876722 )
            return 1;
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        }
        v43 = sub_140FE8230();
        if ( v43 == 0 || *(_BYTE *)(v43 + 47) != 1 )
        {
          *(float *)v63 = (float)*(__int16 *)(a1 + 136) / MEMORY[0x141775530];
          v62 = sub_14083D4F0(v6) + 104;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        v26 = *(_WORD *)(a1 + 140);
        if ( v26 <= 0 )
          v26 = *(_WORD *)(a1 + 136);
      }
      goto LABEL_222;
    }
    if ( a2 > 1399813739 )
    {
      if ( a2 > 1399813997 )
      {
        if ( a2 == 1399813998 )
        {
          v51 = *(_QWORD *)(a1 + 128);
          if ( v51 != 0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v51 + 144LL))(v51, &v62);
            sub_140FEAD00(&v62, &v60);
            sub_14083DFA0(a3, &v60);
            (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v63[0] + 16LL))(v63[0], v63);
          }
          return 1;
        }
        if ( a2 == 1399876690 )
        {
          v29 = sub_140DBC940();
          LODWORD(v63[0]) = ((*(_WORD *)(a1 + 32) & 0x1FF) << 8)
                          | (*(unsigned __int16 *)(a1 + 32) >> 9)
                          | (*(unsigned __int16 *)(a1 + 34) << 17);
          v62 = v29;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
      }
      else
      {
        if ( a2 == 1399813740 )
        {
          LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 155) & 0x20) != 0;
          v62 = sub_14083D4F0(v6) + 24;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        if ( a2 == 1399813993 )
        {
          sub_140FE7660(*(_QWORD *)(a1 + 128), a3);
          return 1;
        }
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 <= 1399747688 )
    {
      if ( a2 == 1399743863 )
      {
        LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 166) & 0x10) != 0;
        v62 = sub_14083D4F0(v6) + 24;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      if ( a2 == 1399744116 )
      {
        LODWORD(v63[0]) = *(char *)(a1 + 165);
        v62 = sub_14083D4F0(v6) + 40;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 == 1399747689 )
    {
      v47 = *(_QWORD *)(a1 + 80);
      if ( v47 != 0 )
        v48 = *(_QWORD *)(v47 + 32);
      else
        v48 = 0;
      sub_140FCC110(v48, a3);
      return 1;
    }
    if ( a2 != 1399813241 )
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    v19 = *(char *)(a1 + 164);
    if ( *(_BYTE *)(a1 + 164) == 0 )
      goto LABEL_205;
    goto LABEL_212;
  }
  if ( a2 <= 1400189488 )
  {
    if ( a2 > 1400071282 )
    {
      if ( a2 > 1400075364 )
      {
        if ( a2 == 1400075365 )
        {
          LODWORD(v63[0]) = *(char *)(a1 + 159);
          v62 = sub_14083D4F0(v6) + 40;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
        if ( a2 == 1400189241 )
        {
          LODWORD(v63[0]) = *(char *)(a1 + 163);
          v62 = sub_14083D4F0(v6) + 40;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
      }
      else
      {
        if ( a2 == 1400071283 )
        {
          sub_1415E7F10(&v62, a1);
          sub_141189510(&v62, a3);
          sub_14093AAF0(&v62);
          return 1;
        }
        if ( a2 == 1400071764 )
        {
          LODWORD(v63[0]) = *(char *)(a1 + 157);
          v62 = sub_14083D4F0(v6) + 40;
          sub_14083DFA0(a3, &v62);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
          return 1;
        }
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 > 1400071019 )
    {
      if ( a2 == 1400071020 )
      {
        sub_141189420(a1, &v60);
        v49 = sub_141335F60();
        LODWORD(v63[0]) = v60;
        v62 = v49;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      if ( a2 == 1400071033 )
      {
        LODWORD(v63[0]) = *(_DWORD *)(a1 + 112);
        v62 = sub_14083D4F0(v6) + 40;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 != 1400005241 )
    {
      if ( a2 == 1400009318 )
      {
        LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 166) & 0x40) != 0;
        v62 = sub_14083D4F0(v6) + 24;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    v6 = *(_WORD *)(a1 + 44) & 0x1FF;
    v19 = 0;
    if ( (_WORD)v6 != 1 )
      v19 = *(unsigned __int16 *)(a1 + 46);
    if ( *(_WORD *)(a1 + 46) != 1900 )
      v19 = *(unsigned __int16 *)(a1 + 46);
    goto LABEL_212;
  }
  if ( a2 <= 1400206193 )
  {
    if ( a2 > 1400204915 )
    {
      if ( a2 == 1400204916 )
      {
        LODWORD(v63[0]) = *(char *)(a1 + 161);
        v62 = sub_14083D4F0(v6) + 40;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      if ( a2 == 1400206184 )
      {
        LOBYTE(v63[0]) = (*(_BYTE *)(a1 + 166) & 2) != 0;
        v62 = sub_14083D4F0(v6) + 24;
        sub_14083DFA0(a3, &v62);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
        return 1;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 == 1400189489 )
    {
      LODWORD(v63[0]) = *(char *)(a1 + 162);
      v62 = sub_14083D4F0(v6) + 40;
      sub_14083DFA0(a3, &v62);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
      return 1;
    }
    if ( a2 != 1400202105 )
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    v19 = *(_DWORD *)(a1 + 116);
    if ( v19 <= 0 )
      goto LABEL_205;
    goto LABEL_212;
  }
  if ( a2 <= 1467310949 )
  {
    if ( a2 != 1400206194 )
    {
      if ( a2 != 1400326477 )
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      v26 = *(_WORD *)(a1 + 142);
      if ( v26 <= 0 )
        goto LABEL_205;
      goto LABEL_222;
    }
    v59 = a3;
    sub_1407C9510(&v62);
    if ( qword_141ABD470 == 0 )
      qword_141ABD470 = sub_1407E4940();
    v60 = 0;
    v61 = 0;
    sub_141189030(a1, &v60);
    v44 = v60;
    if ( *((_QWORD *)&v60 + 1) != (_QWORD)v60 )
    {
      v45 = 1;
      if ( (unsigned __int64)((__int64)(*((_QWORD *)&v60 + 1) - v60) >> 3) >= 2 )
        v45 = (__int64)(*((_QWORD *)&v60 + 1) - v60) >> 3;
      v46 = 0;
      do
      {
        (*(void (__fastcall **)(_QWORD, __int64 *))(**(_QWORD **)(v44 + 8 * v46) + 144LL))(
          *(_QWORD *)(v44 + 8 * v46),
          &v57);
        sub_140FEAD00(&v57, v56);
        sub_14083B5F0(&v62, v56);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v56[0] + 16LL))(v56[0], v56);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v58 + 16LL))(v58, &v58);
        ++v46;
      }
      while ( v45 != v46 );
    }
    sub_14083DB80(&v57, &v62);
    sub_14083DFA0(v59, &v57);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v57 + 16LL))(v57, &v57);
    if ( v44 != 0 )
      sub_1407E4890(qword_141ABD470, v44, v61 - v44);
LABEL_194:
    sub_14083B0A0(&v62);
    return 1;
  }
  switch ( a2 )
  {
    case 1467310950:
      LOBYTE(v63[0]) = (*(_WORD *)(a1 + 166) & 0x800) != 0;
      v62 = sub_14083D4F0(v6) + 24;
      sub_14083DFA0(a3, &v62);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v62 + 16LL))(v62, &v62);
      return 1;
    case 1684303986:
      sub_1407C9510(&v62);
      DWORD2(v60) = 1399026761;
      *(_QWORD *)&v60 = sub_14083D4F0(v36) + 56;
      sub_14083B5F0(&v62, &v60);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
      v38 = sub_14083D4F0(v37);
      DWORD2(v60) = 1398957177;
      *(_QWORD *)&v60 = v38 + 56;
      sub_14083B5F0(&v62, &v60);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
      v40 = sub_14083D4F0(v39);
      DWORD2(v60) = 1399025785;
      *(_QWORD *)&v60 = v40 + 56;
      sub_14083B5F0(&v62, &v60);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
      v42 = sub_14083D4F0(v41);
      DWORD2(v60) = 1400071764;
      *(_QWORD *)&v60 = v42 + 56;
      sub_14083B5F0(&v62, &v60);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
      sub_14083DB80(&v60, &v62);
      sub_14083DFA0(a3, &v60);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
      goto LABEL_194;
    case 1937006948:
      sub_140FE7190(a1, &v62);
      sub_140FEAD00(&v62, &v60);
      sub_14083DFA0(a3, &v60);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v60 + 16LL))(v60, &v60);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v63[0] + 16LL))(v63[0], v63);
      return 1;
    default:
      break;
  }
  return sub_140FE3F20((_DWORD *)a1, a2, a3);
}
