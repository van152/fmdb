char __fastcall sub_141536D80(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  int v6; // eax
  int v7; // ecx
  int v8; // eax
  int v9; // edx
  __int16 v10; // cx
  char v11; // cl
  float v12; // xmm0_4
  __int64 v13; // rbx
  unsigned int v14; // eax
  unsigned int v15; // eax
  int v16; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v17[40]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 > 1667330919 )
  {
    if ( a2 <= 1768845939 )
    {
      if ( a2 > 1668246895 )
      {
        if ( a2 == 1668246896 )
        {
          v13 = qword_141B5FDC0;
          sub_140FE7960(v17, a3, 1668246896);
          *(_QWORD *)(a1 + 32) = sub_140F7A940(v13, v17);
        }
        else
        {
          if ( a2 != 1701733492 )
            return result;
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B5C8D0);
            if ( dword_141B5C8D0 == -1 )
            {
              sub_140DBC9B0(&qword_141B5C8A0);
              sub_141751048(sub_140DBCA10);
              sub_141750EA0(&dword_141B5C8D0);
            }
          }
          if ( (__int64 *)*a3 == &qword_141B5C8A0 )
          {
            v14 = *((_DWORD *)a3 + 2);
            HIWORD(v16) = v14 >> 17;
            LOWORD(v16) = (v14 >> 8) & 0x1FF | ((_WORD)v14 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
          {
            (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v17, a3);
            sub_1413CA830(&v16, v17);
          }
          else
          {
            v16 = 124518401;
          }
          *(_DWORD *)(a1 + 60) = v16;
        }
      }
      else if ( a2 == 1667330920 )
      {
        *(_DWORD *)(a1 + 40) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
      else
      {
        if ( a2 != 1668182625 )
          return result;
        *(_DWORD *)(a1 + 76) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
      return 1;
    }
    if ( a2 > 1937007731 )
    {
      if ( a2 != 1937007732 )
      {
        if ( a2 == 2036687218 )
        {
          v8 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
          v9 = 3;
          if ( (unsigned __int16)(23593 * v8) < 0xA3Eu )
            v9 = 15;
          *(_WORD *)(a1 + 58) = v8;
          v10 = ((v8 & v9) == 0) + 365;
          result = 1;
          if ( v10 == (*(_WORD *)(a1 + 56) & 0x1FF) - 1 )
            *(_WORD *)(a1 + 56) = *(_WORD *)(a1 + 56) & 0xFE00 | v10;
        }
        return result;
      }
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      if ( (__int64 *)*a3 == &qword_141B5C8A0 )
      {
        v15 = *((_DWORD *)a3 + 2);
        HIWORD(v16) = v15 >> 17;
        LOWORD(v16) = (v15 >> 8) & 0x1FF | ((_WORD)v15 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
      {
        (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v17, a3);
        sub_1413CA830(&v16, v17);
      }
      else
      {
        v16 = 124518401;
      }
      *(_DWORD *)(a1 + 56) = v16;
    }
    else
    {
      if ( a2 != 1768845940 )
      {
        if ( a2 != 1936684402 )
          return result;
        *(_BYTE *)(a1 + 94) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        return 1;
      }
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
      {
        v12 = (*(float (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
        *(float *)(a1 + 64) = v12;
        result = 1;
        if ( v12 == 0.0 )
          *(_DWORD *)(a1 + 64) = -1027211264;
        return result;
      }
      *(_DWORD *)(a1 + 64) = -1082130432;
    }
    return 1;
  }
  if ( a2 > 1131639407 )
  {
    if ( a2 > 1131700852 )
    {
      if ( a2 == 1131700853 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_DWORD *)(a1 + 44) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_DWORD *)(a1 + 44) = -1;
      }
      else
      {
        if ( a2 != 1131704940 )
          return result;
        *(_DWORD *)(a1 + 84) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
    }
    else if ( a2 == 1131639408 )
    {
      *(_BYTE *)(a1 + 95) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
    else
    {
      if ( a2 != 1131639417 )
        return result;
      *(_DWORD *)(a1 + 80) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
    return 1;
  }
  if ( a2 > 1131441259 )
  {
    if ( a2 == 1131441260 )
    {
      *(_DWORD *)(a1 + 88) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
    else
    {
      if ( a2 != 1131572578 )
        return result;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
      {
        v6 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        v7 = 1;
        if ( v6 != 0 )
          v7 = v6;
        *(_DWORD *)(a1 + 48) = v7;
      }
      else
      {
        *(_DWORD *)(a1 + 48) = 0;
      }
    }
    return 1;
  }
  if ( a2 != 1129142085 )
  {
    if ( a2 != 1130587745 )
      return result;
    *(_BYTE *)(a1 + 96) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    return 1;
  }
  *(_DWORD *)(a1 + 68) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
  v11 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
  result = 1;
  if ( v11 == 0 )
    *(_DWORD *)(a1 + 68) = -1;
  return result;
}
