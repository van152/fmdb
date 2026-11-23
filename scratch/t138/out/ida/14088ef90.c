__int64 __fastcall sub_14088EF90(_QWORD *a1, unsigned __int8 a2, unsigned __int8 a3, __int64 a4, char a5, char a6)
{
  __int64 result; // rax
  _QWORD *v8; // rsi
  _QWORD *v9; // rsi
  __int64 *v10; // rax
  __int64 *v11; // rdx
  __int64 *v12; // rcx
  __int64 *v13; // rbx
  void (__fastcall ***v14)(_QWORD, __int64); // rcx
  volatile signed __int32 *v15; // rsi
  __int64 v16; // rdx
  __int64 v17; // rcx
  __int64 v18; // rbx
  bool v19; // al
  __int64 v20; // rax
  __int64 v21; // rsi
  __int64 v22; // rcx
  __int64 v23; // rax
  volatile signed __int32 *v24; // rcx
  void (__fastcall ***v25)(_QWORD, __int64); // rcx
  __int64 v26; // rbp
  volatile signed __int32 *v27; // r15
  __int64 v28; // rax
  unsigned __int64 v29; // r12
  volatile signed __int32 *v30; // rbx
  __int64 v31; // rax
  __int64 v32; // rcx
  bool v33; // r15
  int v34; // r8d
  __int64 v35; // rcx
  __int64 *v36; // rsi
  __int64 *i; // rbx
  __int64 v38; // rcx
  __int64 *v39; // rsi
  __int64 *j; // rbx
  __int64 v41; // rcx
  __int64 *v42; // rsi
  __int64 *k; // rbx
  __int64 v44; // rcx
  __int64 (__fastcall ***v45)(_QWORD, __int64); // rcx
  __int64 v48; // [rsp+48h] [rbp-70h] BYREF
  volatile signed __int32 *v49; // [rsp+50h] [rbp-68h] BYREF
  __int64 v50; // [rsp+58h] [rbp-60h] BYREF
  __int64 v51; // [rsp+60h] [rbp-58h] BYREF
  __int64 v52; // [rsp+68h] [rbp-50h]
  _QWORD v53[9]; // [rsp+70h] [rbp-48h] BYREF

  v52 = a4;
  if ( a5 == 0 && a6 == 0 || (_BYTE)(result = (*(__int64 (__fastcall **)(_QWORD *))(*a1 + 256LL))(a1)) == 0 )
  {
    v8 = (_QWORD *)a1[18];
    sub_1400D93A0(a1: a1 + 18, a2: a1 + 18, a3: v8[1]);
    v8[1] = v8;
    *v8 = v8;
    v8[2] = v8;
    a1[19] = 0;
    v9 = (_QWORD *)a1[20];
    sub_1400D93A0(a1: a1 + 20, a2: a1 + 20, a3: v9[1]);
    v9[1] = v9;
    *v9 = v9;
    v9[2] = v9;
    a1[21] = 0;
    v49 = nullptr;
    v10 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    v11 = (__int64 *)v10[1];
    v12 = v10;
    if ( *((_BYTE *)v11 + 25) == 0 )
    {
      v12 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
      do
      {
        v13 = v11 + 2;
        if ( v11[4] >= (unsigned __int64)qword_141B5ACC0 )
        {
          v12 = v11;
          v13 = v11;
        }
        v11 = (__int64 *)*v13;
      }
      while ( *(_BYTE *)(*v13 + 25) == 0 );
    }
    if ( *((_BYTE *)v12 + 25) != 0 || qword_141B5ACC0 < (unsigned __int64)v12[4] || v12 == v10 )
    {
      v48 = 0;
    }
    else
    {
      v20 = v12[5];
      v48 = v20;
      if ( v20 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v20 + 8));
    }
    sub_1407C3450(a1: &v51, a2: &v48, a3: &v49);
    v14 = (void (__fastcall ***)(_QWORD, __int64))v48;
    if ( v48 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v48 + 8)) == 0 )
      (**v14)(a1: v14, a2: 1);
    v15 = v49;
    if ( v49 != nullptr && _InterlockedDecrement(v49) == 0 )
    {
      sub_1408B5D70(a1: *(_QWORD *)(*((_QWORD *)v15 + 1) + 8LL));
      v16 = *((_QWORD *)v15 + 1);
      if ( v16 != 0 )
      {
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v17 = *(_QWORD *)(qword_141ABD470 + 24),
              (unsigned __int64)(*(_QWORD *)(qword_141ABD470 + 32) - v17) >= 0x181)
          && (v18 = *(_QWORD *)(v17 + 384)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v18 + 32, a2: v16 - *(unsigned int *)(v18 + 120));
          v19 = *(_BYTE *)(v18 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) != 0;
          if ( !v19 && *(_BYTE *)(v18 + 97) != 0 )
            sub_1412D33C0(a1: v18);
        }
        else
        {
          MEMORY[0x141948990](a1: v16 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      sub_141750CFC(a1: v15);
    }
    if ( v51 == 0 )
      goto LABEL_109;
    v21 = 0x14191EB1BLL;
    sub_14080D0E0(a1: &v50, a2: 0x14191EB1BLL);
    v49 = (volatile signed __int32 *)0x80100004E554C4CLL;
    sub_1407D0F70(
      a1: (unsigned int)&v49,
      a2: (unsigned int)&v48,
      a3: (unsigned int)&v51,
      a4: (unsigned int)&qword_141B5ACC8,
      a5: (__int64)&v50,
      a6: 4,
      a7: 0,
      a8: 0);
    v22 = a1[25];
    if ( v22 == v48 )
    {
      if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v22)(a1: v22, a2: 1);
      v23 = a1[25];
      if ( v23 == 0 )
        goto LABEL_109;
    }
    else
    {
      if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v22)(a1: v22, a2: 1);
      v23 = v48;
      a1[25] = v48;
      if ( v23 == 0 )
        goto LABEL_109;
    }
    v48 = v23;
    _InterlockedIncrement((volatile signed __int32 *)(v23 + 8));
    sub_1407C5A20(a1: &v49, a2: &v48, a3: &v51, a4: &qword_141B5ACC8);
    v24 = (volatile signed __int32 *)a1[26];
    if ( v24 == v49 )
    {
      if ( v24 != nullptr && _InterlockedDecrement(v24 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v24)(a1: v24, a2: 1);
    }
    else
    {
      if ( v24 != nullptr && _InterlockedDecrement(v24 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v24)(a1: v24, a2: 1);
      a1[26] = v49;
      v49 = nullptr;
    }
    v25 = (void (__fastcall ***)(_QWORD, __int64))v48;
    if ( v48 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v48 + 8)) == 0 )
      (**v25)(a1: v25, a2: 1);
    v26 = a1[26];
    if ( v26 != 0 )
    {
      v49 = nullptr;
      if ( a5 != 0 )
        v21 = 0x1418EEAE0LL;
      sub_14080D0E0(a1: &v48, a2: v21);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *, __int64 *, volatile signed __int32 **, int))(*(_QWORD *)v26 + 216LL))(
        a1: v26,
        a2: &v50,
        a3: &qword_141B59758,
        a4: &v48,
        a5: &v49,
        a6: 1);
      v27 = v49;
      if ( v49 != nullptr )
      {
        v28 = *((_QWORD *)v49 + 1);
        if ( *((_QWORD *)v49 + 2) != v28 )
        {
          v29 = 0;
          do
          {
            v30 = *(volatile signed __int32 **)(v28 + 8 * v29);
            if ( v30 != nullptr )
              _InterlockedIncrement(v30 + 2);
            (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v30 + 16LL))(a1: v30, a2: &v50);
            v31 = v50;
            if ( v50 != 0 )
            {
              v48 = 0;
              _InterlockedIncrement((volatile signed __int32 *)(v50 - 4));
              v32 = v50;
              v48 = v31;
              if ( v50 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v50 - 4)) == 0 )
                sub_1412EC9A0(a1: v32 - 4);
              if ( a5 != 0 )
              {
LABEL_61:
                v33 = true;
                if ( a2 == 0 )
                  v33 = (unsigned int)sub_14080AB90(a1: (unsigned int)&v48, a2: 1100104192, a3: -1, a4: 0, a5: 0) != 0;
                if ( a3 == 0
                  && (unsigned int)sub_14080AB90(a1: (unsigned int)&v48, a2: 1100104186, a3: -1, a4: 0, a5: 0) == 0
                  || !v33 )
                {
                  goto LABEL_75;
                }
                goto LABEL_72;
              }
            }
            else
            {
              v48 = 0;
              if ( a5 != 0 )
                goto LABEL_61;
            }
            sub_14080D0E0(a1: &v50, a2: 0x1418EEAE0LL);
            (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v30 + 24LL))(a1: v30, a2: v53);
            if ( v53[0] != v50 )
            {
              if ( (a3 | a2 ^ 1) == 0 )
              {
                LOBYTE(v34) = (unsigned int)sub_14080AB90(a1: (unsigned int)&v48, a2: 1100104192, a3: -1, a4: 0, a5: 0) != 0;
                goto LABEL_74;
              }
              if ( a2 == 0
                && (unsigned int)sub_14080AB90(a1: (unsigned int)&v48, a2: 1100104192, a3: -1, a4: 0, a5: 0) == 0 )
              {
                goto LABEL_75;
              }
LABEL_72:
              v34 = 0;
LABEL_74:
              sub_14088F770(
                (_DWORD)a1,
                a2: (unsigned int)&v48,
                a3: v34,
                a4: v52,
                a5: (__int64)&qword_141B5A4A0,
                a6: a5,
                a7: a6);
            }
LABEL_75:
            v35 = v48;
            if ( v48 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v48 - 4)) == 0 )
              sub_1412EC9A0(a1: v35 - 4);
            if ( _InterlockedDecrement(v30 + 2) == 0 )
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v30)(a1: v30, a2: 1);
            ++v29;
            v27 = v49;
            v28 = *((_QWORD *)v49 + 1);
          }
          while ( v29 < (*((_QWORD *)v49 + 2) - v28) >> 3 );
        }
        if ( _InterlockedDecrement(v27) == 0 )
        {
          v36 = *((__int64 **)v27 + 7);
          if ( v36 != nullptr )
          {
            for ( i = *((__int64 **)v27 + 8); v36 != i; ++v36 )
            {
              v38 = *v36;
              if ( *v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 8)) == 0 )
                (**(void (__fastcall ***)(__int64, __int64))v38)(a1: v38, a2: 1);
            }
            sub_1407E4890(a1: qword_141ABD470);
            *((_QWORD *)v27 + 9) = 0;
            *((_QWORD *)v27 + 8) = 0;
            *((_QWORD *)v27 + 7) = 0;
          }
          v39 = *((__int64 **)v27 + 4);
          if ( v39 != nullptr )
          {
            for ( j = *((__int64 **)v27 + 5); v39 != j; ++v39 )
            {
              v41 = *v39;
              if ( *v39 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v41 + 8)) == 0 )
                (**(void (__fastcall ***)(__int64, __int64))v41)(a1: v41, a2: 1);
            }
            sub_1407E4890(a1: qword_141ABD470);
            *((_QWORD *)v27 + 6) = 0;
            *((_QWORD *)v27 + 5) = 0;
            *((_QWORD *)v27 + 4) = 0;
          }
          v42 = *((__int64 **)v27 + 1);
          if ( v42 != nullptr )
          {
            for ( k = *((__int64 **)v27 + 2); v42 != k; ++v42 )
            {
              v44 = *v42;
              if ( *v42 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v44 + 8)) == 0 )
                (**(void (__fastcall ***)(__int64, __int64))v44)(a1: v44, a2: 1);
            }
            sub_1407E4890(a1: qword_141ABD470);
            *((_QWORD *)v27 + 3) = 0;
            *((_QWORD *)v27 + 2) = 0;
            *((_QWORD *)v27 + 1) = 0;
          }
          sub_141750CFC(a1: v27);
        }
      }
    }
LABEL_109:
    result = sub_14088FEF0();
    v45 = (__int64 (__fastcall ***)(_QWORD, __int64))v51;
    if ( v51 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v51 + 8)) == 0 )
      return (**v45)(a1: v45, a2: 1);
  }
  return result;
}
