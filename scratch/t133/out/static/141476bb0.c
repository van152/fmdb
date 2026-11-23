__int64 __fastcall sub_141476BB0(__int64 a1)
{
  *(_QWORD *)(a1 + 44) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 52) = 124518401;
  *(_QWORD *)(a1 + 8) = 0;
  *(_BYTE *)(a1 + 60) = 0;
  *(_QWORD *)(a1 + 36) = 0x3F80000000000000LL;
  *(_QWORD *)(a1 + 20) = 0;
  *(_QWORD *)(a1 + 28) = 0;
  *(_DWORD *)(a1 + 16) = 0;
  *(_QWORD *)a1 = 0x1418B82A8LL;
  sub_141758A10(a1: a1 + 64, a2: 0, a3: 504);
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  sub_141758A10(a1: a1 + 568, a2: 0, a3: 1428);
  *(_QWORD *)(a1 + 1996) = 0xFFFFFFFFLL;
  *(_QWORD *)(a1 + 2004) = 0x6400000000LL;
  *(_QWORD *)(a1 + 2012) = 0;
  *(_QWORD *)(a1 + 2020) = 0xFFFFFFFF00000000uLL;
  *(_QWORD *)(a1 + 2028) = -1;
  *(_DWORD *)(a1 + 2036) = 273;
  *(_QWORD *)(a1 + 2040) = 0;
  *(_QWORD *)(a1 + 2048) = 0;
  *(_QWORD *)(a1 + 2056) = 0;
  *(_QWORD *)(a1 + 2064) = 0;
  *(_QWORD *)(a1 + 2072) = 0;
  *(_QWORD *)(a1 + 2080) = 0;
  *(_QWORD *)(a1 + 2088) = 0;
  *(_QWORD *)(a1 + 2096) = 0;
  *(_QWORD *)(a1 + 2104) = 0;
  *(_DWORD *)(a1 + 2112) = -1;
  *(_DWORD *)(a1 + 2164) = 0;
  *(_QWORD *)(a1 + 2156) = 0;
  *(_QWORD *)(a1 + 2148) = 0;
  *(_QWORD *)(a1 + 2140) = 0;
  *(_QWORD *)(a1 + 2132) = 0;
  *(_QWORD *)(a1 + 2124) = 0;
  *(_QWORD *)(a1 + 2116) = 0;
  *(_QWORD *)(a1 + 2168) = 0x7FFFFFFF7FFFFFFFLL;
  *(_DWORD *)(a1 + 2176) = 0;
  *(_QWORD *)(a1 + 2180) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 2188) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 2196) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 2204) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 2212) = 0;
  *(_QWORD *)(a1 + 2218) = 0;
  *(_DWORD *)(a1 + 2226) = 2570;
  *(_WORD *)(a1 + 2230) = -256;
  *(_BYTE *)(a1 + 2232) = 0;
  return a1;
}
